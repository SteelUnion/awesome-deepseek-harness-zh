# DeepSeek Harness 安装教程（Windows / macOS / Linux，2026）

> 返回 [DeepSeek Harness 中文使用指南](../README.md) · 最后核对：2026-10-23（dsh `0.2.1-rc`）· 依据官方仓库 [README](https://github.com/deepseek-ai/deepseek-harness) 和 `apps/desktop`、`apps/cli` 文档

DeepSeek Harness（dsh）有四种装法。**新手直接用桌面版**；开发者用 `npx`；想装 Git 插件、改源码的用源码运行。

| 方式 | 系统 | 需要 Node.js | 自动更新 |
|---|---|:---:|:---:|
| [桌面版](#方式一桌面版推荐新手) | Windows x64、macOS（Apple 芯片 / Intel） | ❌（内置） | ✅ |
| [npx 一行启动](#方式二npx-一行启动) | 全平台 | ✅ | 每次运行取最新 |
| [源码运行](#方式三从源码运行) | 全平台 | ✅ 22.19+ 或 24+ | 手动 `git pull` |
| [Python SDK](#方式四python-sdk) | Linux、macOS 14+、Windows x64 | ❌ | 手动 |

## 方式一：桌面版（推荐新手）

官方下载地址：

- Windows x64：<https://download.deepseek.com/desktop/dsh-latest-windows-x64.exe>（约 265 MB）
- macOS Apple 芯片（M 系列）：<https://download.deepseek.com/desktop/dsh-latest-macos-arm64.dmg>
- macOS Intel：<https://download.deepseek.com/desktop/dsh-latest-macos-x64.dmg>

说明：

- Windows 安装包装在当前用户下，可以自选安装目录。
- 桌面版**自带运行环境**，不用装 Node.js。
- 桌面版启动时自动检查更新（之后约每 10 分钟一次），菜单里也有「Check for Updates」。
- 卸载 Windows 桌面版会删掉应用数据，但**不会删除 dsh 的主目录** `~/.dsh`（里面有你的配置、插件和 Key），需要的话手动删。
- **Linux 目前没有官方桌面版**，请用下面的 npx 或源码方式。

## 方式二：npx 一行启动

官方快速开始用的就是这一行（需要先装 [Node.js](https://nodejs.org/)，建议 22.19 或更新的版本）：

```bash
npx @deepseek-ai/dsh web
```

启动后会自动打开浏览器访问 `http://127.0.0.1:3080`。加 `--no-open` 可以不自动打开浏览器。

> ⚠️ 请用 `http://127.0.0.1:3080` 访问，**不要用 `localhost`**，否则会被拒绝（403）。

**全局安装**（官方文档没写，但发布的包里有 `dsh` 命令，社区里很多人这样用）：

```bash
npm install -g @deepseek-ai/dsh
dsh web
dsh --version
```

国内 npm 下载慢，可以临时用 npmmirror 镜像（这是通用的 npm 做法，不是 dsh 官方说明）：

```bash
npm install -g @deepseek-ai/dsh --registry=https://registry.npmmirror.com
```

**版本标签**：npm 上 `latest` 标签是当前稳定的预览版，`next` 标签是更新的候选版。想试最新的可以用 `npx @deepseek-ai/dsh@next web`，但更容易遇到问题。

## 方式三：从源码运行

适合想改代码、或者要安装 Git 仓库形式插件的人。需要 Node.js `22.19+` 或 `24+`，以及 pnpm：

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

**`pnpm run build` 必须在 `pnpm dsh web` 之前运行**，跳过它是源码启动失败的常见原因。

## 方式四：Python SDK

在 Python 程序里调用 dsh（需要 Python 3.10+）：

```bash
python -m pip install deepseek-harness-sdk
```

它会一起安装同版本的 `deepseek-harness-runtime-bin`，里面带有 `dsh` 命令行。

## 验证安装

```bash
dsh --version
dsh --help
```

## 第一次启动要做的事

1. **填 Key**：Settings → Models，填 DeepSeek API Key 并保存（或者登录 DeepSeek 账号，或[配置其他模型](models.md)）。
2. **选工作区**：点 **Choose workspace** 选择项目文件夹。**没选工作区时输入框是灰的。**
3. **先改隐私设置**：会话日志默认上传，见 [隐私与安全设置](privacy-security.md)。

## 安装卡住怎么办

`npx @deepseek-ai/dsh web` 很久没反应、风扇狂转，是被讨论得最多的安装问题之一（官方讨论区 [#3710](https://github.com/deepseek-ai/deepseek-harness/discussions/3710)、[#4321](https://github.com/deepseek-ai/deepseek-harness/discussions/4321)）。

**原因**：npx 每次都要解析完整的依赖树，而 dsh 由上百个互相依赖的预览版包组成，npm 解析起来很慢，个别情况会卡死。

**按顺序试：**

1. **多等几分钟**，第一次运行慢是正常的。
2. **改用桌面版**（Windows、macOS），完全绕开 npm。
3. **改成全局安装**再运行：`npm install -g @deepseek-ai/dsh`，然后 `dsh web`。讨论区的已采纳答案还加了内存参数（社区做法）：

   ```bash
   # macOS / Linux
   NODE_OPTIONS=--max-old-space-size=8192 npm install -g @deepseek-ai/dsh
   ```

   ```powershell
   # Windows PowerShell
   $env:NODE_OPTIONS="--max-old-space-size=8192"; npm install -g @deepseek-ai/dsh
   ```

4. **用 pnpm 代替 npx**（社区反馈在 macOS 上可行）：`pnpm dlx @deepseek-ai/dsh web`。
5. 国内网络问题：加 `--registry=https://registry.npmmirror.com`，或者设置代理（见下）。

## 用代理

官方文档说明 dsh 会读取 `HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY`、`ALL_PROXY`：

```bash
export HTTPS_PROXY=http://127.0.0.1:7890
dsh web
```

社区还反馈，部分 Node.js 版本需要额外设置 `NODE_USE_ENV_PROXY=1` 才会让请求走代理（讨论区 [#175](https://github.com/deepseek-ai/deepseek-harness/discussions/175)，非官方说明）。

> 注意：代理地址里如果带用户名和密码，dsh 运行的**每条命令都能看到它**，官方文档专门提示过这个风险。

## Windows 常见问题

**选择工作区时文件夹对话框报错**（与 `koffi` 原生模块有关，讨论区 [#30](https://github.com/deepseek-ai/deepseek-harness/discussions/30)）：已采纳的做法是加 `--ignore-scripts` 重装，再在 web 配置里把文件夹选择器换成浏览器版后端：

```bash
npm i -g @deepseek-ai/dsh --ignore-scripts
```

**源码运行报 `--expose-internals is required for HMR service`**（讨论区 [#2699](https://github.com/deepseek-ai/deepseek-harness/discussions/2699)）：截至本文核对时还没有官方修复。Windows 用户建议先用桌面版。

## dsh 的文件放在哪

| 位置 | 内容 |
|---|---|
| `~/.dsh`（Windows 通常是 `%USERPROFILE%\.dsh`），可用环境变量 `DSH_HOME` 改 | dsh 主目录 |
| `~/.dsh/.credentials.yaml` | 在设置页填的 API Key |
| `~/.dsh/profiles/web/` | Web 界面用的配置（`cordis.patch.yml`）和插件 |
| `~/.dsh/skills/` | 全局 Skills |
| `~/.dsh/logs/` | 日志 |

下一步：[配置模型与 API Key](models.md)。
