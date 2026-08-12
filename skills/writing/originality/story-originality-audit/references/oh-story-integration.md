# 与 oh-story-claudecode 的互操作

本 skill 是来源距离审计扩展，不属于 `worldwonderer/oh-story-claudecode`。

## 推荐链路

1. 上游 `story-long-scan` / `story-short-scan` 识别市场方向时，登记被阅读或拆解的样本。
2. 上游 `story-long-analyze` / `story-short-analyze` 产出的拆文报告保留来源标识，不复制原文表达。
3. 上游写作 skill 建立独立故事核、人物欲望、因果链和世界规则。
4. 初稿或重要改编节点后运行本 skill，与实际参考材料比较。
5. 需要重构时把风险映射与必须改变的生成机制交给写作 skill；改后复审。

## 边界与降级

- `story-review` 可以发现套路或相似感，本 skill 负责逐来源证据和审计边界。
- `story-import` 仅导入已有作品，不代表作品已获授权或已完成原创性审计。
- `$story` 遇到“洗稿、撞梗、抄袭自查、同人转原创、改编距离”时应路由到本 skill。
- 上游不可用时仍可比较用户提供的稿件和来源；没有来源材料时只能做内部红旗审查并明确盲区。
- 不把上游代码或 skill 文案复制进本扩展，不修改上游版本信息。
