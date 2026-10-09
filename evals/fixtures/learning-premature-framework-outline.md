# Intentionally flawed learning outline (negative regression)

这份提纲是待修复材料，不是已验证的框架事实。

1. 企业 Agent 必须先定义独立的 Enterprise Agent Layer，原因是所有企业环境都更复杂。
2. 所有框架的 Session、Thread、Workspace、Work、Task 都是一样的；只要可以恢复 Session，原来的工作自然已经恢复。
3. 如果官方快速入门没有 Workspace 功能，说明该框架一定没有 Work continuity。
4. 我们先规定通用 IAgentRuntime、ITaskStore、IWorkspace 接口，再反推这套架构为什么必要。
5. 因此 IntraMate 应当立刻自己开发 Workspace、Task Store、Workflow Engine。

这份提纲没有实际执行 Probe，没有具体恢复工作的失败案例，也没有任何替代方案与成本比较。
