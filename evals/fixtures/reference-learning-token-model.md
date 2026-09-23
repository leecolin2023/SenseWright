# Prior Learning Model — Why LLMs use tokens

这是一个已经形成的 Learning Knowledge Model，供 Practice 转化为演练，不应直接作为答案展示。

核心模型：

1. 神经网络最终处理的是数值表示，人类语言需要先转换为有限、可计算的离散单位。
2. 字符级表示通常词表较小，但会拉长 sequence。
3. 完整词级表示可以缩短某些 sequence，但会造成 vocabulary 膨胀、长尾词和新词处理困难。
4. subword / byte-level tokenization 是 vocabulary size、sequence length、语言覆盖和工程成本之间的折中，不是语言天然的唯一单位。
5. Token 会进一步影响 embedding lookup、context consumption、attention compute、latency 和 API usage accounting。
6. “为什么基于 token”不能只回答“因为 Transformer 只能接收 token”；真正需要理解表示粒度与计算结构之间的 trade-off。

Practice 目标：
不要复述这六条，而是通过模型设计、约束变化、替代方案或面试式追问检验用户是否能自己推出这些关系。
