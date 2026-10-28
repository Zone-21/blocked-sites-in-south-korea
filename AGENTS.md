# DeepSeek 调用规则

- 调用 DeepSeek 默认且仅使用 `deepseek-flash`，通过 `tools/deepseek.py` 调用。
- 未经用户明确授权，不得调用其他 DeepSeek 模型，也不得使用 `deepseek-chat`、`deepseek-reasoner` 等别名。
- 只有用户明确授权了其他模型及其使用范围后，才能在该范围内使用 `--model` 和 `--allow-other-model`；不得自行添加放行参数。
- Flash 出错、不可用或效果不足时，不得自动切换模型。需要其他模型时，先向用户申请授权。
- 不得通过直接 API 请求、其他脚本或修改默认值绕过上述规则。
- 创建这些规则的授权仅允许编辑文件，不代表授权调用其他模型。
- 仅发送任务所需内容，不发送密钥或无关工作区文件。
