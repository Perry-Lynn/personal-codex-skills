# Writing Skills

`skills/writing/` 收录面向中文网络小说的写作辅助、读者体验、语言质量、原创性、平台合规和连载复盘能力。每个子目录只放一个职责明确的 Codex skill，按需安装即可。

## 目录

| 功能目录 | Skill | 适用场景 | 详情 |
|---|---|---|---|
| `prose-style/` | `story-prose-style` | 提取、应用和校准项目文风与角色声纹 | [技能说明](../../docs/skills/story-prose-style.md) |
| `reader-experience/` | `story-reader-cold-read` | 盲读开篇、定位误解、弃读点和悬念问题 | [技能说明](../../docs/skills/story-reader-cold-read.md) |
| `language-quality/` | `story-chinese-proofreading` | 检查错字、病句、指代、标点、数字和专名 | [技能说明](../../docs/skills/story-chinese-proofreading.md) |
| `originality/` | `story-originality-audit` | 比较稿件与已知来源的文字、场景和结构距离 | [技能说明](../../docs/skills/story-originality-audit.md) |
| `publishing-compliance/` | `story-fanqie-compliance` | 做番茄发布前合规、低质和连续性检查 | [技能说明](../../docs/skills/story-fanqie-compliance.md) |
| `performance-diagnostics/` | `story-serial-performance-diagnostics` | 用发布后数据和反馈诊断流失与转化变化 | [技能说明](../../docs/skills/story-serial-performance-diagnostics.md) |

## 目录和安装

例如安装文风 skill：

```bash
cp -R skills/writing/prose-style/story-prose-style ~/.codex/skills/
```

其他 skill 的安装路径就是表格中的功能目录加 skill 名称。安装后重新打开 Codex 任务，使技能清单刷新。

## 推荐顺序

常见的协作链路是：上游 scan/analyze → 上游 write → `prose-style` → `reader-experience` → 上游 review → `originality` → 上游 deslop → `language-quality` → `publishing-compliance` → 发布 → `performance-diagnostics`。

这些 skill 可以独立运行，也可以与 [`worldwonderer/oh-story-claudecode`](https://github.com/worldwonderer/oh-story-claudecode) 配合。完整的上游交接和兼容边界见根目录的 [`docs/oh-story-claudecode-integration.md`](../../docs/oh-story-claudecode-integration.md)。
