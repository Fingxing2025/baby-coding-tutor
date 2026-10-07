# v0.1 交付验证记录

日期：2026-10-08（Asia/Shanghai）。本次完成 Skill 与测试材料制作；以下是已执行的检查，不是虚构的学生试用。

## 已通过

| 检查 | 实际结果 | 范围 |
| --- | --- | --- |
| skill-creator 的 quick_validate.py | `Skill is valid!` | 核心入口的名称、frontmatter、描述及未完成占位校验；不判断教学效果。 |
| 元信息和引用 | 文件夹名等于 name；版本是字符串；界面短描述长度合规；默认提示包含 `$baby-coding-tutor`；本地文档链接存在。 | 格式与可导航性。 |
| 自动检查 | `Ran 11 tests … OK` | 完整安装、重复安装、保留不同版本、缺失目录、三个项目准备、禁止覆盖、ZIP 内容、保留不同/损坏 ZIP、真实 HTTP 页面/API/故障。 |
| 本地入口 | `.agents/skills/baby-coding-tutor` 指向 `../../skills/baby-coding-tutor`，可以读到同一份入口。 | 当前交付目录中的发现位置；未把界面选择器或自动路由写成已验收。 |
| 打包 | `dist/baby-coding-tutor-v0.1.0.zip`，一个顶层 Skill 文件夹，内容与源码一致。 | 包含 Skill 核心、示例及 MIT 许可证；整套 README/测试方案在交付目录。校验值在 [SHA256SUMS.txt](../dist/SHA256SUMS.txt)。 |
| 故障浏览器复现 | Headless Chrome 打开 HTTP 页面，点击“加载笔记”；`/api/note` 返回 404，页面显示 JSON 转换错误。 | 真实点击、请求与页面现象，未使用模拟回复。 |
| 最小修复参照 | 在临时副本把业务请求地址改为 `/api/notes`，重载，再点相同按钮；200、两条笔记、控制台 0 错误/0 警告。 | 只验证夹具的可诊断性及修复参照，没有让教学 Agent 跑完整课程。原始 app.js 仍有故障。 |

为避免无关图标请求干扰初学者，交付夹具加了空图标声明；最初复现记录中有一次 favicon 404，其不是加载失败的根因。重新加载的成功检查没有该噪声。

## 浏览器证据

- [失败时页面快照](../output/playwright/failure.snapshot.yml)：显示转换失败。
- [成功时页面快照](../output/playwright/success.snapshot.yml)：显示“加载完成”、两条标题。
- [请求结果摘要](../output/playwright/network.txt)：来自本次浏览器请求列表。
- [修复后控制台摘要](../output/playwright/console-after.txt)：来自本次 console 输出。
- [业务最小差异](../output/playwright/minimal-fix.diff)：只有地址中增加 `s`。

测试使用临时项目副本、本机服务和独立浏览器会话；完成后关闭测试服务与浏览器。完整多轮教学测试不会复用已修好的副本，使用 `prepare 3` 得到原始故障。

## 尚未完成的效果验收

- 目标大学生的真人使用，以及三个项目各一次完整真人多轮测试。
- 真实模型在多轮中是否稳定遵守额度、跳过、降层、召回、不重复及 Debug 顺序。
- Test 1/2 从空目录建成完整应用，Test 3 在教学过程中修好并完成筛选/友好错误提示。
- 其他宿主平台的发现、安装界面、工具调用和自动触发。

这些按 [测试入口](../tests/README.md) 和 [验收标准](../tests/ACCEPTANCE.md) 执行。只有项目功能与教学行为同时通过，才能宣称教学方案通过；文件和脚本通过不能替代它们。

## 本次环境及复跑

检查运行在 macOS，Python 3.14.6；分发和 HTTP 测试仅用标准库。官方 quick_validate 使用临时环境中的 PyYAML 6.0.3，没有增加 Skill 的运行依赖。浏览器通过 Playwright CLI 使用后台 Chrome，不占用用户浏览器窗口。

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/manage.py prepare 3 --dest "/一个新的测试目录"
```

第一条应出现 11 项 `ok` 和 `OK`；第二条应输出安装位置和 `Prepared Test 3`。之后打开新目录，用 `TASK.md` 开始真正的教学试用。

## 开源发布检查

2026-10-08 增加 MIT 许可证，许可证同时包含在仓库和独立 Skill ZIP 中；归档及 SHA256 已随之更新。补充源码获取、发布包下载和试用反馈入口。

GitHub Actions 在 Ubuntu 的 Python 3.11 / 3.14 上执行相同的 11 项检查，并核对发布归档、许可证及 SHA256。[自动测试工作流](../.github/workflows/tests.yml) 不调用模型，也不把这些检查算作真人教学成功。每次远端运行的状态可在 [Actions](https://github.com/Fingxing2025/baby-coding-tutor/actions) 查看。

临时浏览器原始日志和学习项目目录不进入公开仓库；保留上文列出的整理后验证证据。
