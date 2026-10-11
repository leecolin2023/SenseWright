# 合成代码片段：状态推进与效果不符

以下TypeScript是用于教学的完整片段，不代表某开源项目，亦未运行：

```ts
type Job = { status: "pending" | "done"; result?: string };
async function finish(job: Job, write: () => Promise<string>) {
  job.status = "done";
  job.result = await write();
}
```

需求：只有外部 write 真正成功，任务才能被视为 done。write 可能抛出异常。当前代码先修改状态，后调用 write；如果 write 异常，状态可能仍为 done。不要臆造持久化数据库、事务或真正运行过的测试。