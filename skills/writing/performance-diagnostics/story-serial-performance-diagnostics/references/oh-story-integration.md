# 与 oh-story-claudecode 的互操作

本 skill 是发布后诊断扩展，不属于 `worldwonderer/oh-story-claudecode`。

## 推荐闭环

1. 上游 `story-long-write` / `story-short-write` 创作并发布版本。
2. 本 skill 导入平台导出的章节数据和读者反馈，定位异常区间。
3. 把异常章节交给上游 `story-review` 做有目标的文本审查。
4. 把验证后的修订目标交给对应写作 skill，沿用其 revision 和追踪机制。
5. 发布新版本后继续观察同口径、同窗口指标，完成复盘。

## 边界

- `story-long-scan` / `story-short-scan`：外部榜单与市场方向。
- 本 skill：单部作品发布后的自有表现、漏斗和评论诊断。
- `story-review`：文本问题是否真实存在。
- 写作 skill：执行内容改动并维护连续性。

## 路由与降级

`$story` 遇到“掉量、追读下降、完读率、章留、发布后复盘、评论数据”时应路由到本 skill。上游缺失时直接完成数据分析；没有正文时不做内容归因，没有数据时只建立采集模板和测量计划。
