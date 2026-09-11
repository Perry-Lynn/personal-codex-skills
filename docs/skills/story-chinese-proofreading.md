# story-chinese-proofreading

`story-chinese-proofreading` 负责中文小说的字词句终校，修明确错误，不把人物口语改成书面腔，也不借校对之名重写剧情或统一文风。

## 检查内容

- 错别字、漏字、重字、同音误写和乱码。
- 病句、搭配不当、成分残缺、语序和指代歧义。
- 数字、日期、年龄、单位、量词、专名和称谓一致性。
- 对话标点、成对符号、省略号、破折号和异常空白。
- 修订前后的相邻句主体、时间、方向和持物一致性。

## 触发示例

```text
校对这三章，只修明确的错字和病句，不要润色。

检查人名、称谓、数字和对话标点是否统一。

先给问题表，方言和人物故意说错的话不要动。
```

## 分级与脚本

问题分为 `ERROR`、`AMBIGUOUS`、`CONSISTENCY`、`HANDOFF` 和 `PROTECTED`。静态工具仅捕捉配对符号、异常空白、英文省略号和可疑重复等候选：

```bash
python3 skills/writing/language-quality/story-chinese-proofreading/scripts/chinese_proofread.py <file-or-directory>
```

返回码为 `0`（输入有效且无候选）、`1`（输入有效但发现候选）或 `2`（路径、扩展名、空目录、空白输入、读取或编码错误）。脚本无候选不代表人工语义校对完成；综合审查与连续性交给 `story-review`，去 AI 味后应重新终校。
