# 连载数据契约

## 最低字段

脚本接受 UTF-8 CSV，至少需要：

- `chapter`：章节编号或可排序标识。
- 一个可分析数值列，例如 `readers`、`finishes`、`next_readers`、`impressions`、`clicks`、`shelf_adds` 或自定义字段。

推荐附带 `date`、`title`、`published_at`、`word_count`、`channel`、`cohort` 和版本事件列。

## 常见比率

仅在字段口径一致时计算：

- 点击率 = `clicks / impressions`
- 完读率 = `finishes / readers`
- 下一章率 = `next_readers / readers`
- 加书架率 = `shelf_adds / readers`

不能默认不同平台同名指标具有相同定义。任何自定义比率都应在报告中写出分子、分母和零分母处理方式。

## 数据质量清单

- 是否混入累计值和当日增量。
- 是否在回填完成前截取数据。
- 同一章节是否重复多行，重复代表渠道、日期还是错误。
- 章节重发、改名、拆章后标识是否变化。
- 百分比变化是否由极小分母造成。
- 读者批次是否可比，是否混入不同入口和推荐人群。
