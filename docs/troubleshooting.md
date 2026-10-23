# DeepSeek Harness 常见报错排查（安装卡住、403、模型连不上等）

> 返回 [DeepSeek Harness 中文使用指南](../README.md) · 最后核对：2026-10-23（dsh `0.2.1-rc`）

dsh 官方仓库**关闭了 Issues**，问题都在 [Discussions](https://github.com/deepseek-ai/deepseek-harness/discussions) 里。下面整理了讨论最多的报错，标注了来源帖子编号。「官方」指官方文档写明的做法，「社区」指讨论区网友给出、尚未写进官方文档的做法。

## 安装和启动

| 现象 | 原因 | 处理 | 来源 |
|---|---|---|---|
| `npx @deepseek-ai/dsh web` 很久没反应、卡死 | npx 要解析上百个互相依赖的预览版包 | 多等一会；改用桌面版；或全局安装后运行 `dsh web`；或用 `pnpm dlx`。详见[安装卡住怎么办](install.md#安装卡住怎么办) | 社区，#3710、#4321 |
| 打开网页显示 **403** | 用了 `localhost` | 改用 **`http://127.0.0.1:3080`** | 社区，#175 |
| 源码运行 `pnpm dsh web` 失败 | 没先构建 | 先运行 `pnpm run build` | 官方 README |
| Windows 源码运行报 `--expose-internals is required for HMR service` | 启动时的热更新服务问题 | 暂无官方修复，Windows 用户建议先用桌面版 | 社区，#2699 |
| Windows 选择工作区时文件夹对话框报错 | `koffi` 原生模块问题 | `npm i -g @deepseek-ai/dsh --ignore-scripts`，再按帖子说明换用浏览器版文件夹选择器 | 社区（已采纳），#30 |
| `--host 0.0.0.0` 被拒绝 | 官方有意禁止 | 改用具体 IP，如 `--host 192.168.1.10` | 官方 |
| 更新后报 `Cannot read properties of undefined (reading 'prepare')` | 版本回归问题 | 等官方修复；源码用户可以先退回上一个可用版本 | 社区，#7035 |

## 输入和会话

| 现象 | 原因 | 处理 |
|---|---|---|
| 输入框是灰的，发不了消息 | 还没选工作区 | 点 **Choose workspace** 选项目文件夹（官方） |
| `Output token limit reached` | 单次输出达到 `maxTokens` 上限，**不是上下文满了** | 调大当前模型线路的最大输出，或让它分步输出（社区，#1166） |
| 用非 DeepSeek 模型时反复出现 `sandbox escalation ... not strictly wider` | 权限申请循环 | 暂无官方结论，可以先换回 DeepSeek 模型或调整权限模式（社区，#201） |

## 模型连不上

报错 `DeepSeek API request ... failed` 或 `DeepSeek Messages transport failed`，按顺序检查：

1. **Key 对不对**：到 Settings → Models 重新保存一次 Key。
2. **网络和代理**：需要代理的话设置 `HTTPS_PROXY`（官方）。部分 Node.js 版本还要加 `NODE_USE_ENV_PROXY=1`（社区，#175）。
3. **Key 被别的配置覆盖了**：dsh 找 Key 的顺序是环境变量 → `~/.dsh/.credentials.yaml` → 启动目录的 `.env` → `~/.dsh/.env`。
4. **刚升级完就报错**：`Messages transport failed` 是一个笼统的错误标签（社区，#6987），可能是新版本兼容问题，回讨论区看看有没有同样的反馈。

## 自定义模型相关

| 报错 | 原因 | 处理 |
|---|---|---|
| `MISSING_CREDENTIAL` | Key 没保存，或环境变量没设置 | 重新保存 Key，或设置后重启 dsh |
| `UNKNOWN_MODEL` | 选的模型没加到服务商的 Models 列表 | 在该服务商下添加模型 ID |
| 获取模型列表时 401 | Key 无效 | 换 Key，或手动填写模型 ID |
| 模型不存在 / 无可用渠道 | 在第三方服务里用了 DeepSeek 官方的模型名 | 填第三方服务自己的模型 ID |
| 联网搜索时 401 | 内置搜索把 Key 发到了 DeepSeek 官方 | 关掉内置搜索，见 [联网搜索的坑](models.md#内置联网搜索的坑) |

详细说明见 [配置模型与 API Key](models.md#常见配置错误)。

## 还是解决不了？

- 先在 [官方讨论区](https://github.com/deepseek-ai/deepseek-harness/discussions) 搜一下报错原文
- 或者在本仓库开一个 [Issue](../../../issues)，附上：系统、dsh 版本（`dsh --version`）、安装方式、完整报错（**删掉 Key**）
