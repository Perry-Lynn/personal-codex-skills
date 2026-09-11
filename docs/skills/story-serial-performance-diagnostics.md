# story-serial-performance-diagnostics

`story-serial-performance-diagnostics` 用发布后的真实章节指标和读者反馈定位流失、追读、完读、互动或转化变化。它先核对数据口径和异常位置，再阅读对应正文建立竞争假设，不把相关性冒充因果。

## 适用场景

- 某章后阅读人数或下一章率突然下降。
- 点击、加书架、完读、追读或付费表现改变。
- 需要把评论主题与章节数据放在一起复盘。
- 改名、换封、断更、改发布时间后判断变化来自内容还是流量。

## 触发示例

```text
分析这份章节 CSV，告诉我流失从哪一章开始。

把评论做主题编码，区分内容问题、流量变化和样本噪音。

不要直接重写，先给竞争假设和最小验证方案。
```

## CSV 工具

工具支持自选数值列和显式比率定义：

```bash
python3 skills/writing/performance-diagnostics/story-serial-performance-diagnostics/scripts/serial_metrics.py data.csv --value readers --ratio next_rate=next_readers/readers
```

最低字段和指标口径见 skill 的 `references/data-contract.md`。数据诊断定位异常，`story-review` 验证文本问题，写作 skill 执行内容修订并维护追踪。

脚本按 CSV 原始行顺序计算；缺失、非法、`NaN` 或无穷数值输出为 `null` 并记录行级 `diagnostics`，缺失会断开变化基准。末尾单个 `%` 转为比例（`50%` → `0.5`），普通 `50` 不转换。显式列、比率引用和比率名称必须存在且不重名，零分母为 `null` 并诊断；契约或输入错误返回 `2`，有效分析完成返回 `0`。
