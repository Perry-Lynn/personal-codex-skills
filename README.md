# Personal Codex Skills

一组面向 Codex 的个人 Skills，覆盖中文网络小说创作与发布检查，以及双模型开发协作。每个 skill 都是独立、可安装、可版本化的能力包，包含触发说明、执行流程、参考资料和可重复运行的检查脚本。

当前仓库分为两个用途清晰的目录：

| 顶层目录 | 提供什么 | 目录说明 |
|---|---|---|
| [`skills/writing/`](skills/writing/README.md) | 六个中文网络小说写作与发布辅助 skill | 进入目录查看各功能子目录和安装方式 |
| [`skills/tooling/`](skills/tooling/README.md) | Codex 自身的工具和工作流 skill | 进入目录查看模型路由等开发工具 |

> 这些 skill 提供写作、发布前和 Codex 开发协作辅助，不代表平台官方意见，也不承诺作品一定通过审核或获得推荐。

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
cp -R personal-codex-skills/skills/tooling/model-routing/model-router ~/.codex/skills/
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
ln -s "$(pwd)/personal-codex-skills/skills/tooling/model-routing/model-router" ~/.codex/skills/model-router
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

详细说明按目录维护：先进入上表的目录 README，再进入具体功能目录或技能目录。不要把两个目录混用：`writing` 面向作品内容，`tooling` 面向 Codex 开发过程。

## 仓库结构

```text
skills/
  <category>/
    README.md         # 该类别的总览和子目录导航
    <function>/
      README.md       # 该功能目录的说明（如有）
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

修改 skill 后，使用 Codex `skill-creator` 提供的 `quick_validate.py` 验证目录与 YAML frontmatter。仓库内 Python 脚本仅使用标准库，可直接运行：

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
