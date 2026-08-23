# STeCa: Step-level Trajectory Calibration for LLM Agent Learning

- **Authors**: Hanlin Wang, Jian Wang, et al.
- **Year/Venue**: 2025 / ACL 2025 Findings
- **ArXiv**: [ACL Anthology](https://aclanthology.org/2025.findings-acl.604/)
- **Tags**: #step-level-rl #trajectory-calibration #reflection #offline-learning

## Problem
Agent 探索中的次优 action 如何在不需要 online RL 的情况下识别并纠正？

## Method
**Step-level Calibration Pipeline**:
1. Exploration → Step-level reward comparison → 识别次优 action
2. LLM-driven reflection → 生成改进 action
3. Calibrated trajectory construction → SFT

## Key Results
- Agent benchmarks 上显著提升
- 不需要 online RL（offline pipeline）

## Related Papers
- [[CSO - Verified Critical Step Optimization]] — action swap 验证 critical steps
- [[SPA-RL - Stepwise Progress Attribution]] — online RL 版本
