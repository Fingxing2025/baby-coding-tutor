# 宝宝 Coding Mode / Baby Coding Tutor · v0.1.1

Teach while building. When the teaching is finished, the real project should also be finished.

**会写代码，但不会做项目？**

你会 `if`、`for`、函数，甚至能刷算法题，但面对 npm、React、API、Git 就不知道从哪里开始？这个 Skill 让 AI 和你一起做你想做的项目：先讲当前这一步为什么需要，再真的改代码、运行、看结果。

**项目就是课程。教完时，项目也应该能用了。**

它适合有基础编程经验、缺少软件工程经验的大学生。AI 会实际施工，你不用亲手敲每一行；重要的是知道代码为什么在这里、运行时发生什么。

| 普通 AI Coding 常见体验 | 宝宝 Coding Mode |
| --- | --- |
| 一次改很多文件，最后总结 | 一轮推进一个小目标，动手前解释 |
| 默认你认识工程术语 | 第一次用到时讲到够用 |
| 报错后直接修完 | 先看关键错误、联系原因，再修复验证 |
| 跟不上只能回头问 | 随时跳过、降层解释或继续 |

## 现在怎么开始

需要一个能编辑项目文件、运行程序的 coding agent。首个安装目标是本地 Codex；Skill 本身不锁定编程语言、框架或某个 MCP 工具。

先下载 [v0.1.1 Skill 包](https://github.com/Fingxing2025/baby-coding-tutor/releases/tag/v0.1.1)，解压得到 `baby-coding-tutor` 文件夹，按下面的方法复制即可。想使用测试项目和准备工具，下载 [完整源码 ZIP](https://github.com/Fingxing2025/baby-coding-tutor/archive/refs/heads/main.zip)，或用 Git：

```bash
git clone https://github.com/Fingxing2025/baby-coding-tutor.git
cd baby-coding-tutor
```

Git 是记录文件版本的工具；`clone` 把整个仓库下载到本机，`cd` 进入下载后的目录。后面的工具命令都在这个目录里执行；不用 Git 也能使用 Skill。

### 安装到你的项目（推荐）

把整个 `skills/baby-coding-tutor` 文件夹（或 Skill ZIP 解压出的同名文件夹）复制到你的项目的 `.agents/skills/` 中：

```text
你的项目/
└── .agents/
    └── skills/
        └── baby-coding-tutor/
            ├── SKILL.md
            ├── LICENSE
            ├── agents/openai.yaml
            └── references/
                ├── examples.md
                └── teach-skill.md
```

`.agents` 是项目里的一个文件夹，开头的点在很多系统中表示隐藏文件夹；Skill 放到这里供 Codex 发现。不要只复制 `SKILL.md`，它引用了示例文件。

也可以在本仓库目录里运行：

```bash
python3 scripts/manage.py install --project "/你的项目目录"
```

这会复制 Skill 到指定项目，输出 `Installed:` 和实际位置。已有相同文件时只检查一致性，内容不同就停止，避免覆盖你的版本。没有 Python 时使用上面的文件夹复制方式。

想让所有项目都可用，可以运行 `python3 scripts/manage.py install --user`，安装到 `~/.agents/skills/`。`~` 表示你的个人目录。**项目安装和个人安装选一个即可**，避免同名 Skill 重复出现。安装脚本不会修改 Codex 设置。

本交付目录已经有 `.agents/skills/baby-coding-tutor` 的本地发现入口。你实际做项目时，请在目标项目安装，不要把学习项目写进 Skill 源文件。

### 开始第一段对话

在 Codex 输入以下内容（也可从 Skill 选择器选“宝宝 Coding Mode”）：

```text
使用 $baby-coding-tutor，带我做一个能添加、勾选、删除待办，
刷新后还能保留内容的网页。
我会 C++ 的 if、for、函数，但不会 npm、React、Git。
请边做边教，每次只推进一小步，实际运行验证后停下来。
```

应看到 AI 先说明当前小目标，解释必需概念，然后实际创建少量文件、验证结果。下一步由你调节节奏，不需要先学几十小时课程。

也可以先问一个工程概念，例如“使用 $baby-coding-tutor 教我什么是 Skill，我会 C++，但不知道 Markdown”。它应该从实际问题讲起，补齐当前例子里必要的词和写法；你选择制作之后，才开始创建文件。

v0.1.1 调整了一个关键点：**代码每次少写，不代表解释只能讲几句。** 重要写法在动手前讲清；必要的词义和符号会主动解释，不必等你挨个追问。你已经知道的仍然可以随时跳过。

| 你可以说 | AI 应该做什么 |
| --- | --- |
| 会了 / 跳过 / 这个我知道 | 停止当前解释，继续已经选择的小目标 |
| 继续 | 推进当前例子或项目小步，不无限科普 |
| 再讲白一点 | 用更具体、更少陌生词的方式解释 |
| 这个词是什么意思？ | 拆这个词，再回到当前项目 |
| 暂停 | 停止新开发，保留当前位置 |
| 退出宝宝模式，直接做完 | 按你改变后的意图恢复普通开发 |

跳过不是考试，也不是授权 AI 一次写完整个项目。如果后来卡在跳过的知识上，它可以短暂召回，你仍可以再次跳过。

### 没出现 Skill 或使用其他平台

当前官方文档说明 Codex 会自动检测 Skill 变化；如果没有出现，重启 Codex 后再选择，也可以让 agent 直接读取目标路径的 `SKILL.md` 并遵循它。[Codex / ChatGPT 官方说明](https://learn.chatgpt.com/docs/build-skills)

支持 Agent Skills 的其他宿主可以使用同一个核心文件夹，但发现位置和安装界面由宿主决定。`agents/openai.yaml` 是 OpenAI 的可选界面信息，其他宿主可以忽略。[开放格式](https://agentskills.io/specification)

ChatGPT 桌面版支持独立 Skill；官方目前把网页/移动端的可安装分发放在插件路径。这个交付是本地 Skill 文件夹及 ZIP，**不是已经发布的插件**。不要假设普通聊天上传一个 ZIP 就会注册 Skill。普通纯聊天也不能替代实际文件编辑和运行；可以粘贴指令体验语气，但不能算完整工程测试。[官方适用范围](https://learn.chatgpt.com/docs/build-skills)

## 用三个项目试一下

先读 [测试入口](tests/README.md)。它包含可复制的开场提示、测试时说的话、完成条件和失败标准。

| 测试 | 项目 | 要验证什么 |
| --- | --- | --- |
| [Test 1](tests/projects/01-todo/TEST.md) | 无框架 Todo | 小步开发、跳过、真能完成 |
| [Test 2](tests/projects/02-campus-board/TEST.md) | React + 后台 API 校园留言板 | npm、组件、请求和数据流是否讲清楚 |
| [Test 3](tests/projects/03-reading-debug/TEST.md) | 已有故障的阅读清单 | 异步前置召回、降层解释、透明 Debug |

还有一个短的 [Test 4：教我什么是 Skill](tests/behavior/04-teach-skill.md)，专门检查概念解释、创建前解释、降层和真实调用的区别。它是多轮行为测试，不是第四套应用工程。

在本目录运行下面这条命令，得到独立测试目录（目标必须不存在）：

```bash
python3 scripts/manage.py prepare 1 --dest "/你的测试目录/todo"
```

把 `1` 改为 `2` 或 `3` 即可准备其他测试。脚本复制 Skill 和项目任务；Test 1/2 保持空项目，让代码在教学中长出来；Test 3 带已有故障夹具。打开目标文件夹后，把 `TASK.md` 里的提示发给 AI。测试人员自己的操作脚本在本仓库 `TEST.md`，不用全部发给教学 AI。

## 交付与检查

- [核心规则](skills/baby-coding-tutor/SKILL.md)：所有必需行为及节奏护栏。
- [对话示例](skills/baby-coding-tutor/references/examples.md)：初次启动、跳过、降层、召回、Debug、命令/路径。
- [教 Skill 的示例](skills/baby-coding-tutor/references/teach-skill.md)：先理解，再制作，再实际试用。
- [验收标准](tests/ACCEPTANCE.md)：用实际对话、文件差异和运行结果判断，不能只打勾。
- [格式调研](docs/FORMAT-RESEARCH.md)：2026-10-08 核对的官方来源和迁移边界。
- [本次验证记录](docs/VALIDATION.md)：区分文件/脚本验证与尚待真人完成的教学测试。

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/manage.py package
```

第一条在临时目录检查安装、准备、打包和故障夹具，短暂启动只接收本机请求的服务，结束后关闭。它**不证明学生学会了，也不替代多轮教学测试**。第二条生成 `dist/baby-coding-tutor-v0.1.1.zip`，只有一个 Skill 顶层目录，适合复制、归档或交给支持该格式的宿主。

v0.1 没有 IDE、账号、云沙箱、知识图谱或学习评分；节奏护栏依赖模型遵守指令，不是拦截每次编辑的技术装置。先验证这套共同开发方式是否让人跟得上、项目能不能完成，再决定需要什么功能。

## 开源与反馈

采用 [MIT 许可证](LICENSE)，可以使用、修改和分发，保留许可证及版权声明即可。Skill ZIP 也包含许可证。

欢迎在 [GitHub Issues](https://github.com/Fingxing2025/baby-coding-tutor/issues) 分享试用结果。反馈时带上模型/宿主、用户大概会什么、触发问题的对话片段和实际文件变化；按 [记录表](tests/SESSION-RECORD.md) 记录也可以。先移除密钥、私人信息和不适合公开的项目内容。

改进优先依据真实试用：哪个小步跟不上、跳过后是否还在长讲、有没有先写后教、最后项目是否能用。文件和自动检查通过不能代替教学效果验收。
