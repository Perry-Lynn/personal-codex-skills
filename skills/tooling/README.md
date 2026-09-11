# Tooling Skills

`skills/tooling/` 收录面向 Codex 本身的工具编排和开发工作流，不处理小说正文。当前提供一个模型路由 skill。

## 目录

| 功能目录 | Skill | 适用场景 | 详情 |
|---|---|---|---|
| [`model-routing/`](model-routing/README.md) | `model-router` | 创建 Astra 规划对话和 Luna 实施对话，互读交接并验收 | [目录说明](model-routing/README.md) |

## 安装

```bash
cp -R skills/tooling/model-routing/model-router ~/.codex/skills/
```

安装后重新打开 Codex 任务，使技能清单刷新。
