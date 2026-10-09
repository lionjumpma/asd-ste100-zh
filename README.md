# 简明技术中文

一版受 ASD-STE100 启发、面向中文技术文本的 Agent Skill。它帮助改写 Agent 指令、工具描述、错误消息、操作步骤和状态报告，使执行者、对象、条件和要求强度更明确。

这是一套中文写作方法，不是 ASD-STE100 的官方中文版，也不提供标准合规认证。英文标准的词数上限、时态规则与词典不能直接套用到中文。

## 安装

在需要使用该 skill 的项目目录运行：

    npx skills add lionjumpma/asd-ste100-zh

也可以手动把本仓库的 SKILL.md、scripts/ 和 examples/ 放入同一个 skill 目录。skill 名称是 asd-ste100-zh。

## 使用

示例请求：

- “用简明技术中文改写这段工具说明，保留所有条件和错误码。”
- “审查这份操作步骤有哪些可能误读的地方，先不要改写。”
- “严格模式改写这条 Agent 指令，并给我原文与改写对照。”
- “自然模式整理这段 README，保留技术术语。”

默认返回可直接复制的改写稿。如果原文缺少关键事实，skill 会标出待确认项，不替作者补写。完整规则见 [SKILL.md](SKILL.md)，改写样例见 [examples/before-after.md](examples/before-after.md)。

## 辅助检查脚本

脚本只提示可能含糊的表达，例如“必要时”“它”“无缝”和叠加的不确定词。它不能判断指代是否真的不清楚，也不能验证改写是否保留原意。

    python scripts/zh-lint.py 文档.md
    python scripts/zh-lint.py --json 文档.md
    python scripts/zh-lint.py --selftest

默认只报告，不用发现数决定退出状态。如果要在自动检查中将候选项作为人工审核门槛，可加 --fail-on-findings。

## 来源和许可

本项目改编自 [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)，遵循其 MIT 许可并保留原作者版权声明。ASD-STE100 标准与本项目分别由不同主体维护；正式规则和词典请参阅 [ASD 官方网站](https://asd-ste100.org/)。

本 skill 没有收录官方词典，也没有证据证明使用它后，下游 Agent 的误读率必然下降。重要指令仍需人工核对。
