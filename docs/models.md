# DeepSeek Harness 配置模型与 API Key：DeepSeek、Kimi、GLM、自定义服务

> 返回 [DeepSeek Harness 中文使用指南](../README.md) · 最后核对：2026-10-23（dsh `0.2.1-rc`）· 依据官方文档 `docs/user/guide/providers.md`、`apps/cli/reference`

dsh 本身不带模型，要配好**服务商 + API Key + 模型 ID** 才能用。这篇讲四种情况：DeepSeek 官方、dsh 内置的其他服务商、自定义服务商，以及接入聚合平台。

## DeepSeek 官方（默认）

dsh 默认的服务商叫 `deepseek-official`，走 Anthropic Messages 协议连接 `https://api.deepseek.com/anthropic`。

| 模型 ID | 说明 |
|---|---|
| `deepseek-flash` | 默认模型，支持文本和图片输入 |
| `deepseek-v4-pro` | 更强、更贵 |

**三种填 Key 的方法：**

1. **设置页（推荐）**：Settings → Models → 填 DeepSeek API Key → 保存。Key 存在 `~/.dsh/.credentials.yaml`，设置里只保存引用。
2. **环境变量**：

   ```bash
   export DEEPSEEK_API_KEY=sk-你的Key      # macOS / Linux
   ```

   ```powershell
   $env:DEEPSEEK_API_KEY = "sk-你的Key"     # Windows PowerShell
   ```

3. **DeepSeek 账号登录**：选 `deepseek-account` 方式，在浏览器里授权，不用手动复制 Key。

**dsh 找 Key 的顺序**：当前环境变量 → `~/.dsh/.credentials.yaml` → 启动目录下的 `.env` → `~/.dsh/.env`。排在前面的会覆盖后面的，改了 Key 不生效时先查这个。

**思考强度**：DeepSeek 适配器支持 `reasoningEffort`，可选 `off`、`low`、`high`、`max`。

## dsh 内置的其他服务商

dsh 通过内置的 pi-ai 服务商目录，支持 `moonshotai`（Kimi）、`zai`（智谱 GLM）、`openai`、`anthropic` 等。在 **Settings → Models → Add model provider** 里选择对应服务商，填入它的 API Key 即可。

## 添加自定义服务商（任何 OpenAI / Anthropic 兼容接口）

**界面操作**：Settings → Models → **Add model provider** → **Custom model API**，填写：

| 字段 | 说明 |
|---|---|
| Provider ID | 服务商 ID，小写，**保存后不能改** |
| Display name | 显示名称 |
| Base URL | 接口地址，OpenAI 兼容服务一般带 `/v1` |
| API protocol | `openai-completions`、`openai-responses` 或 `anthropic-messages` |
| API key | 服务商的 Key |
| Models | 模型 ID、显示名、上下文长度、最大输出、输入类型（文本 / 图片）、思考强度 |

填好地址和 Key 后，可以点 **Fetch available models**，它会请求服务商的 `GET /models`，自动列出可用模型。

**配置文件写法**：Web 界面里的「Open configuration file」会打开 `cordis.patch.yml`。

- `~/.dsh/profiles/web/cordis.patch.yml` 只对 Web 界面生效
- `~/.dsh/cordis.patch.yml` 对所有 profile 生效

官方示例：

```yaml
- id: llm-pi-ai
  config:
    providers:
      my-gateway:
        apiKeyEnv: GATEWAY_API_KEY
        api: openai-completions
        baseURL: https://gateway.example/v1
        models:
          - id: legacy-chat
          - id: vision-preview
            input: [text, image]
```

- `apiKeyEnv` 是**存放 Key 的环境变量名**，不是 Key 本身。
- 兼容开关（官方文档列出的）：`compat.supportsDeveloperRole: false`、`compat.maxTokensField: max_tokens`、`compat.thinkingFormat: deepseek`。
- 修改在**下一次请求时生效**。

## 接入第三方 / 聚合平台（以 Orbis 为例）

聚合平台能让你**用一个账户在 dsh 里切换 DeepSeek、Kimi、GLM、Claude、GPT 等模型**。下面以本仓库维护方 [Orbis](https://orbiorbi.com/?utm_source=github&utm_medium=docs&utm_campaign=awesome-deepseek-harness-zh&utm_content=models-orbis) 为例，其他兼容服务改地址和模型 ID 即可。

**1. 准备 Key 和模型 ID**：在 Orbis 的 DeepSeek V4.1 Flash 或 DeepSeek V4 Pro 模型页选一条线路、创建 Key。Orbis 的 Key 绑定线路。**注意 Orbis 的模型 ID 和 DeepSeek 官方不同：**

| 模型 | Orbis 模型 ID | DeepSeek 官方 ID（不要填在 Orbis 里） |
|---|---|---|
| DeepSeek V4.1 Flash | `deepseek-v4.1-flash` | `deepseek-flash` |
| DeepSeek V4 Pro | `deepseek-v4-pro-0813` | `deepseek-v4-pro` |

**2. 添加自定义服务商**：Settings → Models → Add model provider → Custom model API：

| 字段 | 填写 |
|---|---|
| Provider ID | `orbis` |
| Display name | `Orbis` |
| Base URL | `https://api.orbiorbi.com/v1` |
| API protocol | `openai-completions` |
| Credential | 你的 Orbis Key |
| Models | 手动添加 `deepseek-v4.1-flash` |

或者写进 `cordis.patch.yml`（Key 放在环境变量 `ORBIS_API_KEY` 里）：

```yaml
- id: llm-pi-ai
  config:
    providers:
      orbis:
        api: openai-completions
        baseURL: https://api.orbiorbi.com/v1
        apiKeyEnv: ORBIS_API_KEY
        compat:
          thinkingFormat: deepseek
          supportsDeveloperRole: false
          maxTokensField: max_tokens
        models:
          - id: deepseek-v4.1-flash
            input: [text, image]
          - id: deepseek-v4-pro-0813
```

`thinkingFormat: deepseek` 让思考参数按 DeepSeek 的格式发送；`input: [text, image]` 只加在支持图片的模型上（V4.1 Flash 支持，V4 Pro 只支持文本）。

**3. 在会话右下角把模型切到 `orbis` 下的模型。**

**4. 关掉内置联网搜索**（原因见下一节），或者换成第三方搜索插件。

**5. 自检**：用 Key 请求 `GET https://api.orbiorbi.com/v1/models`，返回的列表里应该有你填的模型 ID。完整说明见 [Orbis 文档：DeepSeek Harness 接入](https://orbiorbi.com/docs/deepseek-harness/?utm_source=github&utm_medium=docs&utm_campaign=awesome-deepseek-harness-zh&utm_content=models-orbis)。

> **不要**把第三方的 Key 填进 dsh 自带的 DeepSeek 卡片，也不要只改 `DEEPSEEK_BASE_URL`：dsh 的内置路由会发送 DeepSeek 官方的模型名，第三方服务会返回「模型不存在」。

## 内置联网搜索的坑

dsh 自带的联网搜索插件（`web-search-deepseek`）有三个特点，官方文档里都有写：

1. 它使用 `deepseek-official` 服务商的配置，会把 Key **同时放在 `x-api-key` 和 `Authorization` 两个请求头里**，发到这个服务商配置的地址（默认是 DeepSeek 官方）。
2. **每搜一次都消耗一次完整的模型调用**，搜得多的时候费用不低。
3. 如果你在 DeepSeek 卡片里填了别家的 Key，这个 Key 就会被发到 DeepSeek 官方，然后报 401。

**建议：**

- 只用 DeepSeek 官方：可以保留内置搜索，但注意费用。
- 用第三方服务：在 **Settings → Plugins → Web search** 里关掉内置搜索（配置文件里是禁用 `web-search-deepseek`）。需要联网时，换成 [modsearch](https://github.com/liustack/modsearch) 或 [dsh-free-search](https://github.com/DDDMUC/dsh-free-search) 这类不需要 Key 的搜索插件。
- 已经把第三方 Key 发出去过：在对应平台停用这枚 Key 并新建一个。

## 常见配置错误

| 报错 | 原因 | 处理 |
|---|---|---|
| `MISSING_CREDENTIAL` | 没保存 Key，或 `apiKeyEnv` 指向的环境变量没设置 | 在 Models 页重新保存 Key；用环境变量的话，设置后重启 dsh |
| `UNKNOWN_MODEL` | 会话里选的模型没加到服务商的 Models 列表 | 在该服务商下添加这个模型 ID |
| 获取模型列表时 401 | Key 无效 | 检查 Key；也可以跳过自动获取，手动填模型 ID |
| `model_not_found` / 无可用渠道 | 用了别家的模型 ID，或 Key 所在线路没有这个模型 | 使用服务商模型页给出的 ID |
| 切换思考强度后 400 | 思考参数格式不对 | 在 `compat` 里加 `thinkingFormat: deepseek` |
| 发图片报错 | 模型不支持图片输入 | 只给支持图片的模型加 `input: [text, image]` |

**不知道选哪个模型？** 可以参考 [AI Agent 能力排行榜](https://orbiorbi.com/leaderboards/agent/?utm_source=github&utm_medium=docs&utm_campaign=awesome-deepseek-harness-zh&utm_content=models-choose) 和 [编程排行榜](https://orbiorbi.com/leaderboards/code/?utm_source=github&utm_medium=docs&utm_campaign=awesome-deepseek-harness-zh&utm_content=models-choose)（每日更新，标注数据来源）。
