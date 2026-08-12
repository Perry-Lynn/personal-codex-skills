# story 路由集成

本仓库的六个 story skills 是个人扩展，不属于 `worldwonderer/oh-story-claudecode` 上游包。为让 `$story` 处理模糊意图时能发现它们，本机 `story/SKILL.md` 路由表应保留：

```markdown
| 文风与角色声纹 | 按我的文风、统一文风、文风校准、对白说人话、文风漂移 | `$story-prose-style`（个人扩展） |
| 读者盲读 | 读者视角、盲读、哪里看不懂、弃读点 | `$story-reader-cold-read`（个人扩展） |
| 中文终校 | 校对、错别字、病句、标点、专名统一 | `$story-chinese-proofreading`（个人扩展） |
| 原创性审计 | 洗稿、撞梗、抄袭自查、同人转原创、改编距离 | `$story-originality-audit`（个人扩展） |
| 番茄发布合规 | 番茄审核、推荐被拒、发布前检查、平台规范、恶意水文 | `$story-fanqie-compliance`（个人扩展） |
| 发布后复盘 | 掉量、追读下降、完读、章留、评论数据 | `$story-serial-performance-diagnostics`（个人扩展） |
```

官方 `story` 包更新可能重写其 `SKILL.md`。每次按官方路线更新后：

1. 检查上述六行是否仍在路由表。
2. 缺失时按本文件恢复，不改上游仓库或伪造上游版本。
3. 确认个人 skills 仍安装于 Codex 个人 skills 目录。
4. 重新打开 Codex 任务，使技能清单和路由稳定刷新。

职责分工：

- `$story-prose-style`：建立、应用和校准项目文风。
- `$story-deslop`：清除AI痕迹，不负责定义项目文风。
- `$story-review`：审查结构、逻辑、人物和一致性。
- `$story-reader-cold-read`：隔离作者资料复原真实读者体验。
- `$story-chinese-proofreading`：做字词句、标点和专名终校。
- `$story-originality-audit`：逐来源审查表达与结构距离。
- `$story-fanqie-compliance`：执行番茄发布合规和反水文门禁。
- `$story-serial-performance-diagnostics`：分析发布后真实数据和反馈。

完整流水线、降级与交接协议见仓库 `docs/oh-story-claudecode-integration.md`。
