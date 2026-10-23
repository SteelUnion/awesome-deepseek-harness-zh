# DeepSeek Harness 配置 MCP 服务器教程

> 返回 [DeepSeek Harness 中文使用指南](../README.md) · 最后核对：2026-10-23（dsh `0.2.1-rc`）· 依据官方 `packages/mcp/mcp-client/README.md`

MCP（Model Context Protocol）是一个通用协议，让 AI 工具接入外部能力，比如操作 GitHub、查数据库、读文档。dsh 通过官方插件 `@deepseek-ai/dsh-mcp-client` 接入 MCP 服务器。**默认一个 MCP 服务器都没开**，截至本文核对时也没有找到配置 MCP 的图形界面，需要写配置文件。

## 配置方法

在 `~/.dsh/profiles/web/cordis.patch.yml`（Web 界面的配置，也可以在界面里点「Open configuration file」打开）里，每个 MCP 服务器加一条 `@deepseek-ai/dsh-mcp-client`。官方示例：

```yaml
- id: mcp-github
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    serverName: github
    transport: stdio
    command: npx
    args: ['-y', '@modelcontextprotocol/server-github']
    env:
      GITHUB_TOKEN: !!js process.env.GITHUB_TOKEN
- id: mcp-web
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    serverName: web
    transport: streamable-http
    url: http://localhost:3000/mcp
```

| 字段 | 说明 |
|---|---|
| `id` | 这一条配置的唯一 ID，每个服务器不同 |
| `serverName` | 服务器名，工具会以 `mcp__<serverName>__<工具名>` 的形式出现 |
| `transport` | `stdio`（本地启动一个进程）或 `streamable-http`（连接一个 HTTP 地址） |
| `command` / `args` | `stdio` 方式启动服务器的命令 |
| `url` | `streamable-http` 方式的地址 |
| `env` | 传给服务器的环境变量。`!!js process.env.XXX` 表示从你的环境变量里读，**避免把 Token 写死在文件里** |

其他默认值：工具调用超时 `toolCallTimeoutMs` 为 60000 毫秒，断线重连 `reconnect.maxAttempts` 为 10 次。

## 安全提醒

`stdio` 方式的 MCP 服务器是**在沙箱外运行的可执行程序**，权限和你本人一样。只接入来源可信的服务器，Token 用环境变量传，不要写进配置文件。

## 相关

- 官方 MCP 记忆示例在仓库的 `apps/cli/config/examples/mcp-memory/`
- 想要不写配置、用插件实现的记忆和上下文管理，见 [精选插件：上下文、记忆与省 Token](plugins.md)
