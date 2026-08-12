# Personal Codex Skills

一组面向中文网络小说创作与发布检查的 Codex Skills。每个 skill 都是独立、可安装、可版本化的能力包，包含触发说明、执行流程、参考资料和可重复运行的检查脚本。

当前仓库提供六个互补 skill：

| Skill | 解决什么问题 | 适合什么时候使用 | 当前版本 |
|---|---|---|---|
| [`story-prose-style`](docs/skills/story-prose-style.md) | 建立、应用和校准项目专属文风与角色声纹 | 文风提取、续写前校准、对白口语化、检查文风漂移 | 1.0.2 |
| [`story-reader-cold-read`](docs/skills/story-reader-cold-read.md) | 隔离作者资料，复原读者实际理解与情绪 | 盲读开篇、查弃读点、验证悬念和信息差 | 1.0.0 |
| [`story-chinese-proofreading`](docs/skills/story-chinese-proofreading.md) | 执行中文小说字词句、标点和专名终校 | 错别字、病句、指代歧义、数字单位与称谓统一 | 1.0.0 |
| [`story-originality-audit`](docs/skills/story-originality-audit.md) | 审查稿件与已知来源的表达和结构距离 | 洗稿自查、撞梗判断、同人转原创、改编审计 | 1.0.0 |
| [`story-fanqie-compliance`](docs/skills/story-fanqie-compliance.md) | 执行番茄小说发布前的合规、低质与连续性检查 | 发布前检查、拒审诊断、合规修订、反水文审查 | 1.0.1 |
| [`story-serial-performance-diagnostics`](docs/skills/story-serial-performance-diagnostics.md) | 用发布后数据和反馈诊断流失与转化变化 | 追读下降、完读变化、章留、评论与发布复盘 | 1.0.0 |

> 这些 skill 提供写作与发布前辅助，不代表平台官方意见，也不承诺作品一定通过审核或获得推荐。

## 安装

### 方法一：安装单个 skill

把目标 skill 目录复制到 Codex 的个人 skills 目录：

```bash
git clone https://github.com/Perry-Lynn/personal-codex-skills.git
mkdir -p ~/.codex/skills
cp -R personal-codex-skills/skills/writing/prose-style/story-prose-style ~/.codex/skills/
cp -R personal-codex-skills/skills/writing/reader-experience/story-reader-cold-read ~/.codex/skills/
cp -R personal-codex-skills/skills/writing/language-quality/story-chinese-proofreading ~/.codex/skills/
cp -R personal-codex-skills/skills/writing/originality/story-originality-audit ~/.codex/skills/
cp -R personal-codex-skills/skills/writing/publishing-compliance/story-fanqie-compliance ~/.codex/skills/
cp -R personal-codex-skills/skills/writing/performance-diagnostics/story-serial-performance-diagnostics ~/.codex/skills/
```

只需要其中一个时，只复制对应目录。复制完成后重新打开 Codex 任务，使技能清单刷新。

### 方法二：开发者方式

克隆仓库后，将目标 skill 目录链接到 `~/.codex/skills/`。这样拉取仓库更新后，不需要重复复制文件。

```bash
git clone https://github.com/Perry-Lynn/personal-codex-skills.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/personal-codex-skills/skills/writing/prose-style/story-prose-style" ~/.codex/skills/story-prose-style
ln -s "$(pwd)/personal-codex-skills/skills/writing/reader-experience/story-reader-cold-read" ~/.codex/skills/story-reader-cold-read
ln -s "$(pwd)/personal-codex-skills/skills/writing/language-quality/story-chinese-proofreading" ~/.codex/skills/story-chinese-proofreading
ln -s "$(pwd)/personal-codex-skills/skills/writing/originality/story-originality-audit" ~/.codex/skills/story-originality-audit
ln -s "$(pwd)/personal-codex-skills/skills/writing/publishing-compliance/story-fanqie-compliance" ~/.codex/skills/story-fanqie-compliance
ln -s "$(pwd)/personal-codex-skills/skills/writing/performance-diagnostics/story-serial-performance-diagnostics" ~/.codex/skills/story-serial-performance-diagnostics
```

## 快速使用

安装后直接用自然语言提出任务。Codex 会根据 `SKILL.md` 的描述判断是否调用对应 skill，也可以在请求中点名 skill。

```text
用 story-prose-style 从这三章里提取本书文风，并建立正文文风指纹。

检查第 12 章是否出现文风漂移，先只给报告，不要改正文。

不看大纲，先对前三章做读者盲读，找出最大的弃读点。

校对这份正文，只修明确的错字、病句、标点和专名问题。

比较这份稿件与参考材料，审计原创性距离，不要做表面换词。

用 story-fanqie-compliance 检查这篇短篇能否发布到番茄，列出 BLOCK、FIX 和 REVIEW。

根据平台返回的拒审理由诊断问题，保留剧情功能后做合规修订。

分析章节 CSV 和评论，定位追读下降从哪里开始并给验证方案。
```

## 与 oh-story-claudecode 互补

这些 skills 可与 [`worldwonderer/oh-story-claudecode`](https://github.com/worldwonderer/oh-story-claudecode) 配合使用，但不属于其官方组件，也不复制其扫榜、拆文、写作、连续性、综合审查和去 AI 味能力。

推荐链路是：上游 scan/analyze → 上游 write → 项目文风 → 读者盲读 → 上游 review → 原创性审计 → 上游 deslop → 中文终校 → 番茄合规 → 发布 → 连载数据诊断 → 上游 revision。

完整的路由表、输入输出交接、兼容降级和上游更新注意事项见 [`docs/oh-story-claudecode-integration.md`](docs/oh-story-claudecode-integration.md)。每个个人 skill 即使找不到上游也能独立运行；涉及剧情事实和追踪状态的修改仍交回上游写作流程。

## Skill 说明

### story-prose-style

负责项目专属文风，而不是把所有作品统一成一种“高级感”。它会区分对白声音、叙述声音、句段节奏、题材气质和角色声纹，并把量化指标当作漂移信号，而不是机械写作配额。

- 支持建立文风、应用文风、文风校准、维护指纹和局部回炉。
- 支持长篇、短篇、独立稿件与已有项目。
- 自带 `style_fingerprint.py`，可比较稳定样本与目标章节。
- 默认保留剧情事实和人物动机；涉及连续性变化时交回写作流程处理。

完整说明、示例与脚本用法见 [`docs/skills/story-prose-style.md`](docs/skills/story-prose-style.md)。

### story-reader-cold-read

负责受控读者盲读。第一遍不看作者资料，只记录读者已知、误解、情绪、弃读点和翻页动力；第二遍再与大纲和设定对照，避免作者知识替正文补洞。

完整说明见 [`docs/skills/story-reader-cold-read.md`](docs/skills/story-reader-cold-read.md)。

### story-chinese-proofreading

负责明确语言错误和格式一致性终校，保护角色口语、方言和有意断句。它不会代替综合审查，也不会以“更文学”为理由润色。

完整说明与脚本用法见 [`docs/skills/story-chinese-proofreading.md`](docs/skills/story-chinese-proofreading.md)。

### story-originality-audit

负责逐来源比较文字、场景、结构和生成机制，区分题材惯例、独立表达、来源依赖和高风险近似。工具结果只是候选，不是法律结论。

完整说明与脚本用法见 [`docs/skills/story-originality-audit.md`](docs/skills/story-originality-audit.md)。

### story-fanqie-compliance

负责番茄小说发布前门禁，将平台硬红线、广告引流、现实隐私、恶意水文、故事连续性和去 AI 味前置检查放在同一套流程中。

- 支持写作前约束、发布前审查、拒审诊断、合规修订和规范维护。
- 使用 `BLOCK`、`FIX`、`REVIEW`、`PASS` 四级结论。
- 自带 `fanqie_preflight.py`，检查重复段落、工程词、乱码、明显引流和绕审表达。
- `PASS` 只表示受检范围未发现已定义风险，不代表平台保证通过。

完整说明、示例与脚本用法见 [`docs/skills/story-fanqie-compliance.md`](docs/skills/story-fanqie-compliance.md)。

### story-serial-performance-diagnostics

负责发布后的指标和评论复盘，先核对口径与异常位置，再建立内容、流量、发布和数据竞争假设，并把验证后的修订目标交回写作流程。

完整说明与脚本用法见 [`docs/skills/story-serial-performance-diagnostics.md`](docs/skills/story-serial-performance-diagnostics.md)。

## 仓库结构

```text
skills/
  <category>/
    <function>/
      <skill-name>/
        SKILL.md          # Codex 读取的核心工作流
        VERSION           # skill 的语义化版本
        agents/           # UI 展示元数据
        references/       # 按需加载的规则与判定资料
        scripts/          # 可重复运行的确定性工具
docs/skills/              # 面向使用者的独立说明
registry.yaml             # skill 清单和版本权威来源
CHANGELOG.md              # 发布记录
LICENSE                   # Apache-2.0 许可证
```

## 版本规则

每个 skill 使用独立的[语义化版本](https://semver.org/lang/zh-CN/)：

- `PATCH`：文案修正、规则澄清和向后兼容的问题修复。
- `MINOR`：新增检查项、参考资料、脚本或兼容能力。
- `MAJOR`：工作流、输出契约或目录结构出现不兼容变更。

发布 skill 时需要同步更新其 `VERSION`、`registry.yaml` 和 `CHANGELOG.md`。技能标签采用 `<skill-name>/v<version>`，仓库级版本采用 `repo-v<version>`。

## 开发与验证

修改 skill 后，使用 Codex `skill-creator` 提供的 `quick_validate.py` 验证目录与 YAML frontmatter。仓库内五个 Python 脚本仅使用标准库，可直接运行：

```bash
python3 skills/writing/prose-style/story-prose-style/scripts/style_fingerprint.py --help
python3 skills/writing/language-quality/story-chinese-proofreading/scripts/chinese_proofread.py --help
python3 skills/writing/originality/story-originality-audit/scripts/text_overlap.py --help
python3 skills/writing/publishing-compliance/story-fanqie-compliance/scripts/fanqie_preflight.py --help
python3 skills/writing/performance-diagnostics/story-serial-performance-diagnostics/scripts/serial_metrics.py --help
```

提交新 skill 时，请保持 `SKILL.md` 精简，把只在特定任务中需要的详细规则放入 `references/`，把重复执行且需要确定性的逻辑放入 `scripts/`。

## 规则与责任边界

- 平台规则可能更新。需要实时判断时，应核对平台最新官方规则。
- 不要把静态脚本的无报错等同于人工语义审查通过。
- 不要使用这些 skill 生成违法内容、现实攻击、人肉、侵权材料或绕过平台审核的方法。
- 仓库中的番茄规则文件是执行摘要，不是番茄小说官方文件。

## 许可证

本仓库采用 [Apache License 2.0](LICENSE)。第三方平台名称和规则归各自权利人所有；仓库中的相关摘要仅用于说明检查流程。
