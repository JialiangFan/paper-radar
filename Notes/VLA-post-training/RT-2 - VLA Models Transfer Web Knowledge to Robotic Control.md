# RT-2 - VLA Models Transfer Web Knowledge to Robotic Control

- **Title:** RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- **Authors:** Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, Brianna Zitkovich
- **Venue:** arXiv preprint (arXiv:2307.15818)
- **Year:** 2023
- **Affiliations:** Google DeepMind


## 主题
VLA Web-Knowledge Robotic Control Transfer

## 背景
大规模 vision-language models (VLMs) 在互联网数据上预训练后，具备了强大的视觉理解、语义推理和 open-vocabulary 识别能力，但如何将这些能力迁移到机器人低层控制中仍是一个开放问题。此前的工作（如 RT-1）使用专用 transformer 架构在 robot demonstration 数据上训练策略，但未能利用 web-scale pretraining 所蕴含的丰富语义知识。与此同时，将 LLMs/VLMs 应用于机器人领域的方法大多仅处理高层 planning，低层 controller 本身并不受益于互联网规模的预训练。

## 现有局限与研究问题
- **Limitation:** 现有机器人策略（如 RT-1）仅在有限的 robot demonstration 数据上训练，缺乏对 novel objects、unseen backgrounds 和 new environments 的泛化能力；而已有的 VLM-for-robotics 方法仅将 VLM 用于 high-level planning 或 perception module，低层控制器无法直接继承 web-scale 语义知识。
- **Problem:** 能否将大规模预训练的 VLM 直接整合到 end-to-end 低层机器人控制中，使单一模型既输出 robot actions 又保留从互联网数据中习得的语义推理与泛化能力？

## 贡献
- 提出 Vision-Language-Action (VLA) 模型范式：将 robot actions 表示为 text tokens，与 natural language 共享同一输出空间，从而直接在预训练 VLM 上 co-fine-tune 得到 end-to-end robotic policy。
- 实例化两个 RT-2 变体：RT-2-PaLI-X（5B/55B）和 RT-2-PaLM-E（12B），在不引入额外 action-only 模块的前提下实现 VLA。
- 通过约 6,000 次真实机器人评估，证明 RT-2 在 seen tasks 上与 RT-1 持平，在 unseen objects/backgrounds/environments 上泛化性能提升约 2 倍，并展现出 emergent capabilities（symbol understanding、reasoning、human recognition）。
- 证明 co-fine-tuning（同时使用 web data 和 robot data）优于仅用 robot data fine-tuning，且更大模型带来更好泛化。
- 展示 chain-of-thought reasoning 可集成进 VLA，使 RT-2 在执行动作前先用自然语言生成 plan，从而处理更复杂的语义指令。

## 方法论
- **Action Tokenization:** 将 robot action（6-DoF end-effector 位移 + gripper 开合 + 终止指令）离散化为 256 bins，每个 action 维度映射为一个 integer token，整个 action 表示为 8 个 token 的字符串，与自然语言 token 共享词表。
- **Co-Fine-Tuning:** 在原始 VLM 预训练数据（WebLI 等 web-scale vision-language data）与 robot demonstration 数据上联合微调，采用 VQA 格式（"Q: what action should the robot take to [instruction]? A: [action tokens]"），robot data 在训练 batch 中占约 50%-66% 的采样权重。
- **Output Constraint:** 推理时，当模型被提示执行 robot-action task，通过限制 decoding vocabulary 仅采样合法 action tokens，确保输出可直接在真实机器人上执行。
- **Real-Time Inference:** 最大模型（55B）部署于 multi-TPU cloud service，通过网络查询实现 1-3 Hz closed-loop 控制；5B 版本可达约 5 Hz。
- **Chain-of-Thought 扩展:** 在 fine-tuning 数据中增加 "Plan" 字段，模型先用自然语言输出动作意图，再输出 action tokens，实现多步语义推理（如判断"improvised hammer"应选石头）。
- **Backbone 架构:** RT-2-PaLI-X 基于 ViT-22B encoder + 32B encoder-decoder backbone；RT-2-PaLM-E 基于 ViT + 12B PaLM decoder-only LLM，通过 projection layer 融合视觉与语言 token。
