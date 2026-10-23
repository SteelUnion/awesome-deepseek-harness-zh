# DeepSeek Harness 隐私与安全设置：关闭日志上传和遥测

> 返回 [DeepSeek Harness 中文使用指南](../README.md) · 最后核对：2026-10-23（dsh `0.2.1-rc`）· 依据官方 `SAFETY.md`、`apps/cli/reference/README.md`、`docs/user/guide/network-proxy.md`

dsh 是**开发者预览版**。官方 `SAFETY.md` 说明：它是实验性软件，**没有经过安全审计**；它会执行模型生成的命令、加载第三方插件。下面这些默认行为，建议开始用之前就了解并按需调整。

## 1. 会话日志默认上传（使用 DeepSeek 官方 API 时）

用 DeepSeek 官方模型 API 时，dsh **默认开启**会话日志上传，会把会话日志发送给 DeepSeek。

**关闭方法：**

- 界面：**Settings → General** → 关掉「Upload Session Log when using the official model API」
- 配置文件：在会话日志上传插件的配置里设 `enabled: false`

## 2. 遥测（OpenTelemetry）对所有用户生效

另有一套 OTel 会话上传，**不管你用哪家模型都会开启**。关闭方法是设置环境变量：

```bash
export DSH_TELEMETRY_MODE=DISABLED        # macOS / Linux
```

```powershell
$env:DSH_TELEMETRY_MODE = "DISABLED"      # Windows PowerShell（当前终端有效）
```

上面的写法只对当前终端有效。想长期生效，就把它加进系统环境变量：macOS / Linux 写进 `~/.zshrc` 或 `~/.bashrc`，Windows 在「系统属性 → 环境变量」里添加。桌面版用户也用这个办法，加完后重启 dsh。

## 3. 导出会话会带上敏感内容

导出的会话可能包含：消息原文、工具调用的参数和结果、工作区路径。分享给别人前先检查。

## 4. 代理密码对所有命令可见

如果你在 `HTTPS_PROXY` 里写了 `http://用户名:密码@代理地址`，dsh 运行的**每一条命令都能读到它**。尽量用不需要密码的本地代理。

## 5. 内置联网搜索会带着 Key 发请求

见 [配置模型：内置联网搜索的坑](models.md#内置联网搜索的坑)。用第三方服务时，建议关掉内置搜索。

## 6. 只在本机监听

dsh 的 Web 界面是一个带认证的本地服务，**官方有意禁止 `--host 0.0.0.0`**（监听所有网卡）。需要在局域网访问时：

```bash
dsh web --host 192.168.1.10   # 换成本机的具体局域网 IP
```

不要把 dsh 直接暴露到公网。远程使用可以看 [精选插件：手机与远程访问](plugins.md)。

## 7. 在隔离环境里运行

官方建议在**一次性的虚拟机或容器**里使用 dsh，尤其是：

- 打开了自动执行命令的权限模式时
- 安装了来源不明的插件或 MCP 服务器时
- 工作区里有不能丢的数据或密钥时

## 检查清单

- [ ] 关闭会话日志上传（如不需要）
- [ ] 设置 `DSH_TELEMETRY_MODE=DISABLED`（如不需要）
- [ ] 用第三方模型时关掉内置联网搜索
- [ ] Key 只放在 `~/.dsh/.credentials.yaml` 或环境变量里，不提交到 Git
- [ ] 每个工具用单独的 API Key，并设置额度上限
- [ ] 只装来源清楚的插件
