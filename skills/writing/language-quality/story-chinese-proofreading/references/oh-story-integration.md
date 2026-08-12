# 与 oh-story-claudecode 的互操作

本 skill 是个人互补扩展，不属于 `worldwonderer/oh-story-claudecode`。

## 推荐顺序

1. 上游 `story-long-write` / `story-short-write` 完成正文和连续性事务。
2. 上游 `story-review` 完成综合审查。
3. 必要时运行上游 `story-deslop`，先处理 AI 模板痕迹。
4. 运行本 skill 做最终字词句、标点和专名校对。
5. 面向番茄发布时，再运行 `story-fanqie-compliance` 做平台门禁；合规修订若改动正文，回到本 skill 复校改动处。

## 路由和降级

- `$story` 识别“校对、错别字、病句、终校、只改明确错误”时，应路由到 `$story-chinese-proofreading`。
- 上游可用时读取其规范正文和项目权威资料，但不修改上游 skill 文件。
- 上游不可用时对用户点名稿件独立运行，以正文建立临时专名表。
- 脚本只产生候选；任何跨章事实冲突交给 `story-review`，任何剧情改写交给写作 skill。

## 交接格式

交回上游时提供：文件与位置、原文、问题类型、为什么不是单纯语言修正、需要保持的事实或人物状态。不要直接改上游派生追踪文件。
