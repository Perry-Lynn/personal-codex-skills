# Model Routing

这个目录提供 `model-router`，用于把一个复杂开发目标交给两个独立的 Codex 对话协作完成。默认分工是：

- Astra（`gpt-6-astra`，`low`）负责只读分析、制定方案和最终审查。
- Luna（`gpt-5.6-luna`，`high`）负责读取方案、修改代码、调试和测试。

每次使用时都可以指定谁来规划、谁来实施，并覆盖任一角色的模型和推理强度；也可以交换 Astra 与 Luna 的职责。只指定一侧时，另一侧沿用默认值。

完整工作流、交接 ID、工作树边界和恢复规则见 [`model-router/SKILL.md`](model-router/SKILL.md)；面向使用者的说明见根目录 [`docs/skills/model-router.md`](../../../docs/skills/model-router.md)。

## 安装

```bash
cp -R skills/tooling/model-routing/model-router ~/.codex/skills/
```

## 使用示例

```text
使用 $model-router，为这个功能创建两个独立 Codex 对话。
由 Astra 制定方案，发送给 Luna；由 Luna 实现并测试，再交回 Astra 审查。
```

也可以显式指定配置：

```text
Planner: gpt-6-astra / low
Executor: gpt-5.6-luna / high
```

这个 skill 只在用户明确要求创建两个对话时创建任务。它不能修改当前对话模型或全局 `config.toml`；如果任务工具不支持双对话，会明确报告阻塞。
