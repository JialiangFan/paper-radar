# ImageNet: A Large-Scale Hierarchical Image Database

## 基本信息

| 属性 | 内容 |
|------|------|
| **作者** | Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, Li Fei-Fei |
| **发表年份** | 2009 |
| **发表会议** | IEEE Conference on Computer Vision and Pattern Recognition (CVPR) |
| **引用量** | 50,000+ |
| **论文链接** | [IEEE Xplore](https://ieeexplore.ieee.org/document/5206848) |

## 核心问题

计算机视觉研究缺乏一个大规模、高质量、层次化的图像数据集来推动算法发展。

## 主要贡献

### 1. 大规模图像数据集
- **1400万+张**标注图像
- **21,841个**类别（synsets）
- 基于WordNet的层次化语义结构
- 通过Amazon Mechanical Turk进行众包标注

### 2. ImageNet Large Scale Visual Recognition Challenge (ILSVRC)
从2010年开始举办年度竞赛：
- **1000个类别**，120万训练图像
- 分类任务（Classification）
- 检测任务（Detection）
- 定位任务（Localization）

### 3. 数据驱动AI的典范
ImageNet证明了**数据规模**对AI性能的决定性影响——大数据+深度学习的组合远超小数据+精巧算法。

## ILSVRC历年突破

| 年份 | 方法 | Top-5错误率 | 里程碑 |
|------|------|-------------|--------|
| 2010 | 传统方法 | 28.2% | 首届竞赛 |
| 2011 | 传统方法 | 25.8% | - |
| 2012 | **AlexNet** | **16.4%** | **深度学习爆发** |
| 2013 | ZFNet | 14.8% | - |
| 2014 | GoogLeNet/VGG | 6.7% | - |
| 2015 | **ResNet** | **3.6%** | **超越人类(5.1%)** |
| 2017 | SENet | 2.3% | 最后一届 |

## 历史意义

- 是计算机视觉领域的**"登月计划"**
- 李飞飞的远见——"我们不需要更好的算法，我们需要更好的数据"
- ILSVRC竞赛直接催生了AlexNet、VGG、GoogLeNet、ResNet等里程碑架构
- 确立了**基准测试驱动研究进步**的范式

## 与后续工作的关联

- AlexNet（2012）在ImageNet上的突破引爆了深度学习革命
- ImageNet预训练模型成为计算机视觉的标准起点（迁移学习）
- 启发了NLP领域的大规模数据集构建（如Common Crawl用于GPT训练）

#AI #dataset #computer-vision #ImageNet #benchmark
