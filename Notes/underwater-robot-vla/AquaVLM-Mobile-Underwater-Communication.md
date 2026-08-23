# AquaVLM - Mobile VLM for Underwater Situation Awareness

## 主题
Mobile VLM underwater messaging

## 背景
水肺潜水等水下活动每年吸引数千万人参与，潜水员之间维持 situation awareness 与有效通信对安全至关重要。传统方案要么依赖手势/灯光等 device-free 信号（信息量有限），要么使用昂贵笨重的 underwater talking device，而近期基于智能手机的声学 messaging 系统（如 AquaApp）只能发送 predefined 文本，无法表达上下文相关的细节。作者来自 University of Illinois Urbana-Champaign，论文将于 ACM Multimedia Systems 2026 (Hong Kong) 发表（arXiv:2510.21722）。

## 现有局限与研究问题
- **Limitation:** 现有水下通信方法在 ubiquity 与 informativeness 之间无法兼得：device-free 手势距离短且信息有限；underwater talking device 价格高（>\$1000）且笨重；diving computer messaging 价格高且仅支持 ~10 条预设短消息；mobile-phone-based app（AquaApp）虽然便宜普及但只能传输 predefined messages，无法生成 context-aware 内容。同时，水下场景中触屏失灵、按键稀少使得文本输入几乎不可行；mobile VLM 缺乏水下领域的 generalization，且对声学信道带来的 bit-level 传输错误十分敏感。
- **Problem:** 能否让潜水员仅用普及的 mobile device，以"tap-and-send"的极简交互在水下高效共享 context-rich 信息，从而提升 situational awareness？换言之，如何在严格的算力、带宽、屏幕、错误率约束下，使 mobile VLM 自动生成并可靠传输与潜水情境相符的简短消息？

## 贡献
- 提出 **AquaVLM**——首个利用 mobile VLM 的水下通信系统，潜水员只需选择 purpose 并 tap 即可让手机基于 image+sensor 自动生成 context-aware 消息并通过 acoustic 信号收发，实现 "tap-and-send" 范式。
- 设计 **context-aware instruction tuning** pipeline：使用 ChatGPT-4o 自动构建涵盖 sender message generation / reply generation / message recovery 三类子任务的水下多模态对话语料（共 16k+21k+48k = 85k 条 LoRA 微调数据），并按 safety / navigation / environment / equipment 四类 purpose 进行 hierarchical message generation，将候选消息从 8 缩减至 2，显著降低算力开销。
- 提出 **error-resilient fine-tuning**：在 PHY 层 CSS 调制下，对 0%–20% BER 范围内的字符级 corruption 数据微调 VLM，使其像人类一样从乱码中恢复语义，这是首个针对 VLM 文本传输的错误鲁棒性微调工作。
- 同时构建 **VR 仿真平台**（Unity + Meta Quest 3，含 Shark Encounter / Tank Leakage / Shipwreck Discovery / Kelp Forest 四种事件）和 **iOS 原型**（iPhone 12 Pro + Apple Watch Ultra，MobileVLMV2-3B 4-bit GGUF 经 LLMFarm 部署），通过 20 名用户主观实验和真实湖泊实验综合评估，验证了 70%–80% purpose-align rate、20m 内 BER<3%、15m 内语义相似度>90% 等关键指标。

## 方法论
- **整体架构 (System Overview).** 离线阶段对 COTS mobile VLM (MobileVLMV2-3B) 做 task-specific instruction tuning；在线阶段，发送端手机/手表采集 image 与 sensor data → VLM 根据所选 purpose 生成 2 条候选消息 → 用户 tap 选择 → channel coding & CSS modulation → 麦克风/扬声器声学传输 → 接收端解调 → VLM 做 message recovery 与 reply generation → 显示给接收方选择回复。
- **Multimodal data preparation.** 从 5 个潜水视频中提取 1,368 关键帧，覆盖多种场景；从 diving watch 的常用 9 个关键参数（深度、温度、tank pressure、NDL 等）合成 sensor 数据，模拟 descent / exploration / ascent / safety stop / completion 等阶段。
- **Conversation generation.** 使用 ChatGPT-4o 配合精心设计的 prompts 与 few-shot examples，分两步生成对话：(1) sender message generation 基于 diver #1 的 intent + 图像 + 传感器数据生成 2 条消息；(2) reply generation 基于 diver #2 的 intent 与传感器数据回复。chain-of-thought 的子任务划分提高 diversity 并减少 formatting 错误。
- **Instruction tuning.** 三类任务（sender / reply / recovery）合并成 85k 条 instruction-answer 数据，使用 **LoRA**（rank=64, lr=4e-5, cosine warm-up 0.03, AdamW）冻结 vision encoder，只微调语言部分；2× RTX 4090 训练 1 epoch ~4 小时。
- **Hierarchical message generation.** 定义四类 purpose（safety / navigation / environment / equipment）作为 prompt 一部分，将候选数从 8 减到 2；推理时用 threshold-based 规则只保留异常或危险 sensor 读数（如 water temp <15°C 或 tank pressure <700 psi），把潜水常识隐式注入 VLM，避免无关数据干扰。
- **Error-resilient fine-tuning.** 构建 PHY 层传输 pipeline（编码→调制→解调→解码），将数值转为 spelled-out 文本（如 "12.1" → "twelve point one"）以增强鲁棒性；用 CSS chirp spreading（SF=5, BW=2 kHz, 312 bps）调制；在 0–20% 区间以 1% 步长扫 BER，对 sender/reply 子集随机加扰生成 48,000 对 corrupted–original 消息，与其他任务数据合并微调，让 VLM 学会逐字符纠错。
- **VR Simulation Platform.** Unity + Meta Quest 3，使用 photorealistic 3D 资产 + 真实水下音轨；事件随机触发；前端帧由后端 server 渲染并经 AirLink 串流，避免眩晕；用 swimming 手势识别替代手柄；用真实手机延迟 trace emulate 端到端延迟。
- **iOS Prototype.** iPhone 12 Pro + Apple Watch Ultra，Swift/SwiftUI + Metal API + Accelerate；watch 通过声学链路向 phone 发送传感数据；手机放入触控防水袋；4-bit 量化的 MobileVLMV2-3B 用 llama.cpp 转 GGUF 后通过 LLMFarm 部署。
- **Transmission pipeline.** 4/7 Hamming + CSS 调制，spreading factor SF=5、bandwidth 2 kHz、312 bps；插入 training symbol 做时间均衡；packet 头加 preamble；接收端做 sync / equalization / demodulation / decoding，再交给 VLM 做语义级 recovery。
- **Evaluation.**
  - *用户研究 (n=20, 13M/7F, 18–35 岁)*：5 分钟教程后，参与者在 VR 中遇到 2–3 个事件，使用 AquaVLM 与模拟潜伴沟通，再用 9 题问卷（1–5 MOS）评估。Purpose-align rate 70%–80%，casual 类最高、navigation 与 status 较低；MOS 在 interaction、immersiveness、overall 上均较高，responsiveness 因延迟相对较低。
  - *Real-world (湖泊, 最大 20m, 平均深 3m)*：与 baseline AquaApp+ 对比，传输 100 轮消息；AquaVLM 在 20m 内 BER <3%、15m 内语义相似度 >90%，远优于 AquaApp+；通过 200 对消息的二次主观研究确定 92% 相似度为"语义相同"阈值；改变深度、朝向、加速度（2–2.5 m/s²）时性能仍稳健（BER<2%）。
  - *指标*：purpose-align rate、responsiveness、interaction、immersiveness、overall MOS、BER、语义相似度（all-MiniLM-L6-v2 cosine）、one-round latency。
