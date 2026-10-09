# Synthetic source contradicting an expected Agent loop (NOT a real product)
All code is a deliberately minimal, local fixture. No external repository evidence is provided.

```ts
// toy/model-only-agent.ts: L01-L09
async function respond(question: string) {
  const answer = await model.generate(question);
  history.push({ role: "assistant", text: answer.text });
  return answer.text;
}
// This file contains no tool schema publication, tool dispatcher,
// tool-result message, executor, retry loop or feedback step.
```

A teammate asserts: “Since the function is named `respond` and keeps history, this is a full Decision → Action → Observation → Decision Agent loop.” The provided source does not support that assertion.
