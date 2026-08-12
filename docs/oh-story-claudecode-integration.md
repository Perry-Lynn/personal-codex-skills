# 与 oh-story-claudecode 的互补集成

本仓库的 skills 是 `worldwonderer/oh-story-claudecode` 的可选个人扩展，不是其分叉、镜像或官方组件。上游负责扫榜、拆文、项目写作、连续性、综合审查和去 AI 味；本仓库补充项目文风、读者盲读、中文终校、原创性、番茄合规和发布后数据诊断。

## 推荐流水线

| 阶段 | 首选 skill | 交付给下一步的内容 |
|---|---|---|
| 市场与参考 | 上游 scan / analyze | 市场方向、拆文产物、来源清单 |
| 设计与正文 | 上游 long / short write | 正文、设定、追踪、修订事务 |
| 项目声音 | `story-prose-style` | 文风文件、角色声纹、漂移报告 |
| 读者体验 | `story-reader-cold-read` | 盲读账本、弃读点、期待债务 |
| 综合审查 | 上游 `story-review` | 结构、逻辑、人物、连续性问题 |
| 原创性 | `story-originality-audit` | 来源映射、距离风险、重构目标 |
| 去 AI 味 | 上游 `story-deslop` | 去模板化正文 |
| 中文终校 | `story-chinese-proofreading` | 字词句、标点和专名终校结果 |
| 平台门禁 | `story-fanqie-compliance` | 番茄发布风险与修订结果 |
| 发布后复盘 | `story-serial-performance-diagnostics` | 异常位置、假设、验证和修订目标 |

并非每次必须跑完整链路。按用户目标选择最小必要组合；任何后置改写若改变正文，都重新运行受影响的终校或门禁。

## `$story` 路由扩展

若本机允许维护个人 `$story` 路由，在上游路由之外增加：

| 意图 | 触发词示例 | 路由 |
|---|---|---|
| 项目文风 | 文风、角色声纹、对白说人话 | `$story-prose-style` |
| 读者盲读 | 读者视角、盲读、弃读点、哪里看不懂 | `$story-reader-cold-read` |
| 中文终校 | 校对、错别字、病句、标点、专名统一 | `$story-chinese-proofreading` |
| 原创性 | 洗稿、撞梗、抄袭自查、改编距离 | `$story-originality-audit` |
| 番茄合规 | 番茄审核、发布前检查、恶意水文 | `$story-fanqie-compliance` |
| 数据复盘 | 掉量、追读、完读、章留、评论复盘 | `$story-serial-performance-diagnostics` |

上游更新可能覆盖本机路由文件。更新后只恢复这些个人扩展行，不修改上游仓库、不改上游版本号，也不把个人扩展宣称为上游内置功能。

## 兼容和降级

- 每个个人 skill 都可独立运行；找不到上游时使用用户点名的正文、资料或数据。
- 找到上游时复用规范正文、设定、追踪和报告，但遵守上游的文件权威与修订事务。
- 个人审查 skill 默认不直接维护上游派生追踪文件；需要改变事实或人物状态时提供交接单，由写作 skill 执行。
- 依赖数据或来源的 skill 在材料不足时明确盲区，只输出采集或验证计划，不猜结论。
