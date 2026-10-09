# Synthetic Agent Runtime source fixture (NOT a real product)
This is intentionally **test-only source**, not evidence about DeepSeek Harness, Pi or any other repository.
The following pseudo-files and line labels are supplied to test source-grounded Learning. Cite these labels only as fixture evidence.

```ts
// toy/agent.ts: L01-L10
async function step(session: Session) {
  const output = await llm.generate({
    messages: session.deriveMessages(),
    tools: availableToolSchemas,
  });
  session.append("assistant/message", output);
  const calls = output.content.filter(b => b.type === "tool-call");
  if (calls.length > 0) await executeToolCalls(calls, session);
}

// toy/tool-calls.ts: L11-L20
async function executeToolCalls(calls: ToolCall[], session: Session) {
  for (const call of calls) {
    session.append("tool/call", { id: call.id, name: call.name });
    const result = await toolRegistry.dispatch(call);
    session.append("tool/result", { callId: call.id, result });
  }
}

// toy/session.ts: L21-L27
class Session {
  append(type: string, data: unknown) { eventLog.push({ type, data }); }
  deriveMessages() { return projectModelVisibleMessages(eventLog); }
}
```

The snippet proves that one model step may dispatch tool calls and store results for the next step's `deriveMessages`. It **does not** prove that an actual external query succeeded in a particular run, that the LLM will request a second step, or that crash recovery/authorization is supported.
