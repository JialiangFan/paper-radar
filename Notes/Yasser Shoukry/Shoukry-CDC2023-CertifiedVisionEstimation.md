# Certified Vision-based State Estimation for Safety-Critical Systems

## 主题
为基于视觉的状态估计器提供认证的正确性保证

## 背景
自动驾驶和机器人系统越来越依赖基于视觉的状态估计（如深度学习感知模型）。然而，DNN 感知模型的输出可能在对抗扰动或自然分布偏移下产生大误差，威胁下游控制系统的安全性。需要对感知模型的输出提供认证的误差界。

## 现有局限与研究问题
- **Limitation:** 标准 NN 鲁棒性验证关注分类准确性，不直接适用于连续输出的状态估计问题；现有感知验证方法忽略了感知误差对下游控制的影响；缺乏端到端的感知-控制安全保证。
- **Problem:** 如何为基于视觉的状态估计器提供认证的输出误差界，并将该保证传播到下游控制系统的安全分析中？

## 贡献
- 提出 certified vision-based state estimation 框架
- 使用 NN 验证器计算感知模型在给定输入扰动下的输出范围（状态估计误差界）
- 将感知误差界传播到控制系统的可达性分析中，实现端到端安全验证
- 在自动驾驶场景中验证方法的实用性

## 方法论
- **感知模型形式化：** 将视觉状态估计器建模为函数 ê = f_NN(I)，其中 I 为输入图像，ê 为估计状态。扰动模型：I' = I + δ，||δ|| ≤ ε
- **输出范围分析：** 使用 BERN-NN 或其他 NN 验证器计算 f_NN 在扰动输入集 {I + δ : ||δ|| ≤ ε} 上的输出范围 [ê_min, ê_max]。这给出了状态估计的认证误差界
- **误差传播：** 将感知误差界作为控制系统的状态不确定性输入。使用可达性分析（如 star set 传播）计算闭环系统在感知不确定性下的可达集
- **安全判定：** 如果可达集与不安全区域不相交，则系统在给定感知扰动下是安全的
- **评估：** 在基于 CNN 的车道检测和位姿估计任务上测试，方法可认证感知模型在 ε-球内的状态估计误差 < 安全阈值

> **Title:** Certified Vision-based State Estimation for Autonomous Landing Systems using Reachability Analysis
> **Authors:** Ulices Santa Cruz Leal, Yasser Shoukry
> **Venue:** IEEE Conference on Decision and Control (CDC 2023)
> **Year:** 2023
> **Affiliations:** University of California, Irvine