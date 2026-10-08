# 当前 Skill 格式核对

核对日期：2026-10-08。查阅并打开以下原始官方页面，未沿用旧文章中的安装路径：

| 来源 | 本版采用的结论 |
| --- | --- |
| [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills) | Skill 是文件夹，入口含名称、描述和指令；先发现元信息，再按需加载正文与资源。Codex 当前推荐项目 `.agents/skills`、个人 `~/.agents/skills`；支持符号链接。 |
| [Agent Skills 规范](https://agentskills.io/specification)（OpenAI 文档链接的开放规范） | 名称与文件夹匹配，最多 64 字符；描述非空、最多 1024 字符；Markdown 正文可链接 references。metadata 的值为字符串。 |
| [OpenAI API：Skills](https://developers.openai.com/api/docs/guides/tools-skills) | API 使用相同核心格式；上传 ZIP 包含一个顶层 Skill 文件夹，上传/版本管理与本地目录发现是不同路径。 |

## 本版结构与判断

```text
baby-coding-tutor/
├── SKILL.md
├── LICENSE
├── agents/openai.yaml
└── references/
    ├── examples.md
    └── teach-skill.md
```

核心入口使用 `name`、`description`、`license` 和 `metadata.version`，不引入实验性的工具白名单或平台专用运行器。界面文件包含显示名、短说明、默认提示；保持默认的自动匹配，用清晰触发描述限制在共同学习的开发任务中。显式用本模式学习工程概念时尊重该任务范围。示例按需加载，核心规则始终在入口内。

Codex 文档旧地址 `https://developers.openai.com/codex/skills` 本次打开重定向到上表的 Build skills；当前页面采用 `.agents/skills`。因此安装脚本采用当前路径，不将过去常见的 `.codex/skills` 写成首选。本机附带的 skill-creator 工具用于创建和格式校验，但安装位置按新文档。

## 平台边界

核心 Agent Skills 文件夹可以迁移到支持该标准的宿主；发现路径、执行工具和界面文件支持情况仍由宿主决定。这是格式兼容，不是已完成各平台运行验收。[开放规范](https://agentskills.io/specification)

官方区分独立 Skill 和插件：桌面、Codex CLI/IDE 可用独立 Skill；可安装的跨网页/移动端分发采用插件。v0.1 先交付本地核心和单目录 ZIP，不添加插件市场发布或额外服务。未验证的界面不提供猜测的“上传即安装”步骤。[官方说明](https://learn.chatgpt.com/docs/build-skills)

API 上传同样不等于获得用户电脑的文件/运行权限，教学使用还需要实际编辑与执行环境。没有这些工具时，只能体验解释流程，不能声称真实项目已完成。[API Skills](https://developers.openai.com/api/docs/guides/tools-skills)
