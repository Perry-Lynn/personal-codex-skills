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

克隆仓库后，选择一个写作 skill 复制到 Codex 的个人 skills 目录：

```bash
git clone https://github.com/Perry-Lynn/personal-codex-skills.git
mkdir -p ~/.codex/skills
cp -R skills/writing/prose-style/story-prose-style ~/.codex/skills/
```

其他 skill 的安装路径就是表格中的功能目录加 skill 名称。也可以将目录链接到 `~/.codex/skills/`，便于跟随仓库更新。安装后重新打开 Codex 任务，使技能清单刷新。

## 快速使用

安装后直接用自然语言提出任务，也可以点名 skill：

```text
用 story-prose-style 从这三章里提取本书文风，并建立正文文风指纹。

不看大纲，先对前三章做读者盲读，找出最大的弃读点。

校对这份正文，只修明确的错字、病句、标点和专名问题。

比较这份稿件与参考材料，审计原创性距离，不要做表面换词。

用 story-fanqie-compliance 检查这篇短篇能否发布到番茄，列出 BLOCK、FIX 和 REVIEW。

分析章节 CSV 和评论，定位追读下降从哪里开始并给验证方案。
```

## 推荐顺序

常见的协作链路是：上游 scan/analyze → 上游 write → `prose-style` → `reader-experience` → 上游 review → `originality` → 上游 deslop → `language-quality` → `publishing-compliance` → 发布 → `performance-diagnostics`。

这些 skill 可以独立运行，也可以与 [`worldwonderer/oh-story-claudecode`](https://github.com/worldwonderer/oh-story-claudecode) 配合。完整的上游交接和兼容边界见根目录的 [`docs/oh-story-claudecode-integration.md`](../../docs/oh-story-claudecode-integration.md)。

## 开发与验证

修改本目录下的 skill 后，使用 Codex `skill-creator` 的 `quick_validate.py` 检查目录和 YAML frontmatter。仓库内写作脚本仅使用标准库，可检查帮助信息：

```bash
for d in skills/writing/*/*; do
  [ -f "$d/SKILL.md" ] && python3 /Users/fupengyu/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d"
done
python3 skills/writing/prose-style/story-prose-style/scripts/style_fingerprint.py --help
python3 skills/writing/language-quality/story-chinese-proofreading/scripts/chinese_proofread.py --help
python3 skills/writing/originality/story-originality-audit/scripts/text_overlap.py --help
python3 skills/writing/publishing-compliance/story-fanqie-compliance/scripts/fanqie_preflight.py --help
python3 skills/writing/performance-diagnostics/story-serial-performance-diagnostics/scripts/serial_metrics.py --help
```

脚本无报错只证明命令和输入格式可用，不替代人工语义审查或平台最终判断。平台规则可能更新，需要实时判断时核对最新官方规则。
