# model-router

`model-router` 是一个 Codex 开发协作 skill，用两个独立对话分工完成复杂开发任务：

- Astra（`gpt-6-astra`，`low`）负责只读分析、方案和最终审查。
- Luna（`gpt-5.6-luna`，`high`）负责读取方案、修改代码、调试和测试。

两个对话通过 `send_message_to_thread` 交换带有交接 ID 的计划和结果。Planner 只读，Executor 是唯一业务代码写入者。技能会记录真实 `threadId` 和 `hostId`，处理异步创建、状态等待、重复消息和不同工作树，避免把未执行的模型切换或验证说成已完成。

## 使用

在 Codex 中明确提出需要双对话协作，例如：

```text
使用 $model-router，为这个功能创建两个独立 Codex 对话。
由 Astra 制定方案，发送给 Luna；由 Luna 实现并测试，再交回 Astra 审查。
```

创建任务是有用户可见副作用的操作。只在用户明确要求创建两个对话时创建；仅要求规划或“先不改代码”时停在规划阶段。两个对话不可用时报告阻塞，不静默改成单模型流程。

## 边界

Skill 不能改变当前对话模型，也不修改全局 `config.toml`。`thinking` 是 Codex 任务工具使用的推理强度字段，对应用户所说的 `reasoning_effort`。工具未提供后端模型身份元数据时，应说明只能确认调用参数被接受。

它不替代项目自身的构建、测试、安全或发布规则；Executor 仍须按实际项目选择验证命令。用户现有改动、权限和项目隔离优先于路由约定。
