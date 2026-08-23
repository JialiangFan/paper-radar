# ShieldNN: Provably Safe Neural Network Filter for Safety-Critical Control

## 主题
可证明安全的神经网络过滤器，在线修正不安全控制动作

## 背景
学习型控制器（如 RL 策略、神经网络控制器）在训练后可能产生不安全的控制动作。安全过滤器（safety filter）作为控制器和执行器之间的中间层，拦截不安全动作并修正为安全替代。传统安全过滤器基于优化求解（如 CBF-QP），实时性受限；神经网络过滤器速度快但缺乏安全保证。

## 现有局限与研究问题
- **Limitation:** 基于优化的安全过滤器（CBF-QP）在高频控制中计算开销过大；现有神经网络安全过滤器通过训练逼近 CBF-QP 解，但无法保证逼近的正确性；缺乏对 NN 过滤器本身的形式化安全保证。
- **Problem:** 如何设计一个神经网络安全过滤器，既有 NN 的实时推理速度，又有可证明的安全保证？

## 贡献
- 提出 ShieldNN：可证明安全的神经网络安全过滤器
- 将 NN 过滤器训练与形式化验证结合，确保过滤后的动作始终安全
- 设计训练-验证-修正的迭代流程，直到 NN 过滤器通过完整安全验证
- 推理速度比 CBF-QP 快 10-100 倍，同时提供等价的安全保证

## 方法论
- **CBF-QP 参考：** 首先构建基于控制屏障函数的二次规划（CBF-QP）安全过滤器作为参考 oracle。CBF-QP 保证：如果当前状态在安全集内，则过滤后的动作使系统保持在安全集内
- **NN 过滤器训练：** 训练 NN 逼近 CBF-QP 的输入-输出映射。训练数据通过在状态空间中采样并求解 CBF-QP 获得
- **形式化验证：** 使用 BERN-NN 验证框架验证训练好的 NN 过滤器是否满足 CBF 安全条件：对所有安全集内的状态，NN 过滤器的输出使 CBF 约束 ḣ(x) + α(h(x)) ≥ 0 成立
- **验证引导修正：** 如果验证发现反例（违反安全条件的状态），将反例加入训练集重新训练。迭代直到验证通过
- **混合执行：** 在验证未完全通过的极端状态区域，回退到 CBF-QP 求解，确保任何时刻都有安全保证
- **评估：** 在倒立摆、自适应巡航控制和无人机控制上测试，ShieldNN 推理时间 < 0.1ms（vs CBF-QP 的 1-10ms），安全性与 CBF-QP 等价

> **Title:** ShieldNN: A Provably Safe NN Filter for Unsafe NN Controllers
> **Authors:** James Ferlez, Mahmoud Elnaggar, Yasser Shoukry, Cody Fleming
> **Venue:** American Control Conference (ACC 2025) / arXiv:2006.09564
> **Year:** 2025
> **Affiliations:** University of California, Irvine