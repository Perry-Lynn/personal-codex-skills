# story 路由集成

`story-prose-style` 和 `story-fanqie-compliance` 是个人扩展，不属于 `worldwonderer/oh-story-claudecode` 上游包。为让 `$story` 处理模糊意图时能发现它们，本机 `story/SKILL.md` 路由表应保留：

```markdown
| 文风与角色声纹 | 按我的文风、统一文风、文风校准、对白说人话、文风漂移 | `$story-prose-style`（个人扩展） |
| 番茄发布合规 | 番茄审核、推荐被拒、发布前检查、平台规范、恶意水文 | `$story-fanqie-compliance`（个人扩展） |
```

官方 `story` 包更新可能重写其 `SKILL.md`。每次按官方路线更新后：

1. 检查上述两行是否仍在路由表。
2. 缺失时按本文件恢复，不改上游仓库或伪造上游版本。
3. 确认个人 skills 仍安装于 Codex 个人 skills 目录。
4. 重新打开 Codex 任务，使技能清单和路由稳定刷新。

职责分工：

- `$story-prose-style`：建立、应用和校准项目文风。
- `$story-deslop`：清除AI痕迹，不负责定义项目文风。
- `$story-review`：审查结构、逻辑、人物和一致性。
- `$story-fanqie-compliance`：执行番茄发布合规和反水文门禁。
