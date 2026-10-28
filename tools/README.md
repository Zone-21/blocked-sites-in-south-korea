# DeepSeek 辅助工具

仅依赖 Python 3 标准库，通过命令调用 DeepSeek，不会自动注册为 Codex 内置子代理。

## 环境配置

1. 在云环境 Secrets 中添加 `DEEPSEEK_API_KEY`，值使用 DeepSeek 平台生成的 API 密钥。
2. 若环境使用网络白名单，追加 `api.deepseek.com`，保留原有域名和预设。
3. 保存并应用配置；若界面要求，重新创建环境。

不要把密钥写入文件、命令参数或聊天，也不要提交到 Git。脚本继承环境的代理和 CA 配置，不关闭 TLS 验证。

## 使用

在仓库根目录执行：

```bash
python3 tools/deepseek.py --check
python3 tools/deepseek.py '请检查以下设计的边界条件：……'
python3 tools/deepseek.py --model deepseek-flash '请分析以下问题：……'
python3 tools/deepseek.py < question.txt
```

`--check` 只检查环境变量是否存在，不发送 API 请求，也不验证密钥有效性。
默认模型为 `deepseek-flash`，不使用 `deepseek-chat` 等别名。指定其他模型时，脚本会在发送请求前拒绝调用。
只有用户明确授权了其他模型及使用范围后，才可以同时使用 `--model` 和 `--allow-other-model` 放行。
该参数是显式放行开关，脚本无法自行验证聊天中的授权；调用者必须遵守仓库 `AGENTS.md` 中的规则。
Flash 调用失败时，不自动切换到其他模型。
默认输出上限为 16384 tokens，超时为 120 秒，分别用 `--max-tokens` 和 `--timeout` 调整。
脚本不自动重试，避免重复费用。

执行调用会把明确提供的提示词发送给 DeepSeek，并产生该账号的 API 费用。
工具不会自动读取其他工作区文件或执行模型输出的命令。
成功时将模型回复写入标准输出并返回退出码 `0`；请求失败返回 `1`，缺少密钥或参数无效返回 `2`。
错误信息不输出密钥、响应正文或响应头。

## 持久化

### 工作区统一入口

执行以下命令，将当前版本脚本及调用规则安装到整个 `/workspace`：

```bash
python3 tools/install_workspace_defaults.py
python3 /workspace/tools/deepseek.py '请分析这个问题：……'
```

安装后，`/workspace/AGENTS.md` 为工作区所有项目指定默认模型 `deepseek-flash` 和输出上限 `16384`。
安装程序保留该文件中的其他指令，重复运行会更新本工具的指令块及脚本副本。
更新仓库脚本后需要重新安装，以同步统一入口。

这属于工作区默认值和智能体指令，不是 DeepSeek 服务端权限策略，也不能强制其他程序采用相同参数。
环境重建可能清除这些文件。初始化入口 `tools/init_environment.sh` 会进入指定仓库、检出 `work` 分支并执行安装。
在本仓库已克隆且检出包含该脚本的版本时，可从任意目录执行：

```bash
bash /workspace/blocked-sites-in-south-korea/tools/init_environment.sh
```

若环境最初检出的是其他分支，为避免找不到入口脚本，请在环境配置的初始化命令中直接填写：

```bash
set -e
cd /workspace/blocked-sites-in-south-korea
git checkout work
python3 tools/install_workspace_defaults.py
```

仓库必须已由平台克隆，且本地 `work` 或可跟踪的 `origin/work` 分支必须存在。
初始化不强制重置文件，也不自动拉取远端更新；检出失败时立即停止，不继续安装。
将脚本提交到仓库不会自动注册平台初始化钩子；当前工具无法代为修改云环境的初始化配置。

这两个文件保存在仓库的 `tools/` 目录中。重建环境后，克隆或检出包含它们的分支即可恢复；密钥仍需通过环境 Secrets 配置。
