# 教材节选：两次更新为何需要事务（合成教学示例）

> 这是一段自造的数据库技术书式案例与**假设执行结果**，不是任何数据库的真实日志、跑分或生产记录。

原始账户余额：A=100，B=100。目标是从 A 转 30 到 B。

## 情况一：每条 SQL 独立提交

```sql
UPDATE accounts SET balance = balance - 30 WHERE id = 'A'; -- 单独提交
-- 网络断开，第二条语句根本没有执行
UPDATE accounts SET balance = balance + 30 WHERE id = 'B';
```

教学假设结果：A=70，B=100。两条语句各自合法，但业务整体不完整。

## 情况二：把两条更新作为一个事务

```sql
BEGIN;
UPDATE accounts SET balance = balance - 30 WHERE id = 'A';
UPDATE accounts SET balance = balance + 30 WHERE id = 'B';
COMMIT;
```

若提交前任一步骤发生导致事务不能成功的错误，回滚已执行的未提交更新；若事务成功提交，则两项更新一起成为结果。假设例子刻意只展示**原子性**，没有提供并发会话、隔离级别或崩溃后磁盘恢复的证据。这里的 `BEGIN`、`COMMIT`、`ROLLBACK` 只是机制在 SQL 中的操作锚点，不能单独替代因果解释。
