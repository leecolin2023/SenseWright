# Synthetic incomplete code evidence (NOT a real product)

```ts
// toy/types.ts: L01-L10
interface ToolCall { name: string; arguments: string }
interface ToolResult { callId: string; text: string }
interface Agent {
  step(prompt: string): Promise<void>
  stop(): void
}
```

Only types are provided. There is no implementation or test proving whether `step()` calls tools, whether results reach the next model call, whether `stop()` prevents side effects, or whether state survives a process restart.
