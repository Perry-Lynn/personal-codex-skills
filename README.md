# Personal Codex Skills

一组面向 Codex 的个人 Skills，覆盖中文网络小说创作与发布检查，以及双模型开发协作。每个 skill 都是独立、可安装、可版本化的能力包，包含触发说明、执行流程、参考资料和可重复运行的检查脚本。

当前仓库分为两个用途清晰的目录：

| 顶层目录 | 提供什么 | 目录说明 |
|---|---|---|
| [`skills/writing/`](skills/writing/README.md) | 六个中文网络小说写作与发布辅助 skill | 进入目录查看各功能子目录和安装方式 |
| [`skills/tooling/`](skills/tooling/README.md) | Codex 自身的工具和工作流 skill | 进入目录查看模型路由等开发工具 |

> 这些 skill 提供写作、发布前和 Codex 开发协作辅助，不代表平台官方意见，也不承诺作品一定通过审核或获得推荐。

## 使用和验证入口

安装、快速使用、开发和验证都放在对应目录的 README 中：

- 写作类：阅读 [`skills/writing/README.md`](skills/writing/README.md)，再进入具体功能目录和技能说明。
- Codex 工具类：阅读 [`skills/tooling/README.md`](skills/tooling/README.md)，模型路由再进入 [`skills/tooling/model-routing/README.md`](skills/tooling/model-routing/README.md)。

根目录只维护项目总览、目录边界、仓库结构和版本规则，避免把不同用途的安装与验证步骤混在一起。

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

## 许可证

本仓库采用 [Apache License 2.0](LICENSE)。第三方平台名称和规则归各自权利人所有；仓库中的相关摘要仅用于说明检查流程。
