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

## `serial_metrics.py` 运行契约

- 按 CSV 原始行顺序计算；不排序，也不跨 `cohort` 或其他分组聚合。
- `50%` 转为 `0.5`，普通 `50` 保持为 `50`；非法、`NaN`、无穷、缺失值均为 `null`，并写入行级 `diagnostics`。
- 变化只比较紧邻上一行的同一列；当前行或上一行缺失/非法时为 `null`，且该行会更新基准为缺失，禁止跨缺失行比较。
- CSV 输入表头和显式列不得使用 `chapter`、`diagnostics`、结果保留字段或任意 `*_change` 派生字段。比率名称与 `NAME=NUM/DEN` 引用必须存在且不重名；比率名称不得覆盖这些字段；零分母为 `null` 并附诊断。
- 均值使用缩放后的稳定求和，有限输入不会仅因求和溢出生成非标准 JSON。返回码 `0` 表示有效分析完成，`2` 表示输入或契约错误；JSON 使用非标准浮点值禁用（`allow_nan=False`）。
