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
python3 tools/deepseek.py --model deepseek-reasoner '请分析以下问题：……'
python3 tools/deepseek.py < question.txt
```

`--check` 只检查环境变量是否存在，不发送 API 请求，也不验证密钥有效性。
默认模型为 `deepseek-chat`，可通过 `--model` 指定账号支持的模型；服务端可能返回实际使用的其他模型名称。
默认输出上限为 2048 tokens，超时为 120 秒，分别用 `--max-tokens` 和 `--timeout` 调整。
脚本不自动重试，避免重复费用。

执行调用会把明确提供的提示词发送给 DeepSeek，并产生该账号的 API 费用。
工具不会自动读取其他工作区文件或执行模型输出的命令。
成功时将模型回复写入标准输出并返回退出码 `0`；请求失败返回 `1`，缺少密钥或参数无效返回 `2`。
错误信息不输出密钥、响应正文或响应头。

## 持久化

这两个文件保存在仓库的 `tools/` 目录中。重建环境后，克隆或检出包含它们的分支即可恢复；密钥仍需通过环境 Secrets 配置。
