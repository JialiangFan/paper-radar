# Formal Methods in Robot Policy Learning and Verification: A Survey

- **Year/Venue**: 2026
- **ArXiv**: [2602.06971](https://arxiv.org/abs/2602.06971)
- **Tags**: #survey #formal-methods #temporal-logic #robot-learning

## Scope
全面综述形式化方法在 robot policy learning 中的应用，包括：

### Specification-Conditioned Policy Training
- **Word2Vec-style embeddings** of STL specs
- **PCA-based encodings** of temporal logic
- **GNN representations** of specification automata
- 将形式化规约作为策略的 conditioning input

### Runtime Monitoring
- 用 learned dynamics model 做在线安全监控
- STL/LTL 在线验证

### Key Categories
1. **CBF-based**: Control Barrier Functions
2. **Temporal logic-based**: LTL, STL, CTL
3. **Lyapunov-based**: Stability certificates
4. **Reachability-based**: Hamilton-Jacobi analysis

## Relevance
**最全面的综述**——理解整个 formal methods + robot learning 的全景。对定位研究空白非常有用。

## Related Papers
- [[robotics-safety-post-training/papers/SELP|SELP]] — LTL 应用实例
- [[robotics-safety-post-training/papers/STL-Decision-Transformer|STL-DT]] — STL 应用实例
- [[robotics-safety-post-training/papers/Neural-Lyapunov-Barrier|Neural Lyapunov Barrier]] — Lyapunov 应用实例
- [[robotics-safety-post-training/papers/SECURE|SECURE]] — CBF 应用实例
