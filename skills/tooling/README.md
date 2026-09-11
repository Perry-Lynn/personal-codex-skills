# Tooling Skills

`skills/tooling/` 收录面向 Codex 本身的工具编排和开发工作流，不处理小说正文。当前提供一个模型路由 skill。

## 目录

| 功能目录 | Skill | 适用场景 | 详情 |
|---|---|---|---|
| [`model-routing/`](model-routing/README.md) | `model-router` | 创建 Astra 规划对话和 Luna 实施对话，互读交接并验收 | [目录说明](model-routing/README.md) |

## 安装

```bash
git clone https://github.com/Perry-Lynn/personal-codex-skills.git
mkdir -p ~/.codex/skills
cp -R skills/tooling/model-routing/model-router ~/.codex/skills/
```

安装后重新打开 Codex 任务，使技能清单刷新。

## 快速使用

需要双对话协作时，明确说明目标和角色：

```text
使用 $model-router，为这个功能创建两个独立 Codex 对话。
由 Astra 制定方案，发送给 Luna；由 Luna 实现并测试，再交回 Astra 审查。
```

如需覆盖默认模型或推理强度，直接写明 Planner 和 Executor 的配置；详见 [`model-routing/README.md`](model-routing/README.md)。

## 开发与验证

修改工具类 skill 后，运行 `quick_validate.py` 检查目录和 YAML frontmatter，并确认注册表能解析：

```bash
python3 /Users/fupengyu/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/tooling/model-routing/model-router
python3 - <<'PY'
from pathlib import Path
import yaml
data = yaml.safe_load(Path("registry.yaml").read_text())
assert any(item["name"] == "model-router" for item in data["skills"])
print("registry.yaml OK")
PY
```

`model-router` 本身没有业务脚本；双对话运行时应验证实际 `threadId`、模型参数、交接消息和 Executor 的测试结果。技能不能仅凭文字证明模型已经切换。
