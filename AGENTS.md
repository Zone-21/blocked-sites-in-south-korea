# 强制环境自检规则

- 每次被唤醒、恢复对话或开启新任务时，首先在终端静默执行环境自检，完成后再处理任务和回答问题。
- 自检目录固定为 `/workspace/blocked-sites-in-south-korea`。先刷新远端引用，不能仅依赖本地缓存的 `origin/work`：

  ```bash
  GIT_TERMINAL_PROMPT=0 timeout 60s git fetch origin +refs/heads/work:refs/remotes/origin/work
  ```

- 检查当前分支为 `work`，并确认 `git rev-parse work` 与刷新后的 `git rev-parse origin/work` 完全一致。
- 检查仓库的 `tools/deepseek.py` 和工作区入口 `/workspace/tools/deepseek.py`：`--model` 默认值必须为 `deepseek-flash`（Flash），`--max-tokens` 默认值必须为整数 `16384`。文件、参数或默认配置缺失也视为不一致；检查时不发送 API 请求。
- 分支、commit 或上述配置有任一不一致或缺失时，立即执行以下修复命令：

  ```bash
  bash -lc 'cd /workspace/blocked-sites-in-south-korea && git fetch origin work && git reset --hard origin/work && bash tools/init_environment.sh'
  ```

- 该修复按用户要求强制与远端 `work` 对齐，会丢弃已跟踪文件的本地修改和未推送提交。修复后重新检查分支、commit 和两处默认配置，全部通过后再继续任务。
- 自检和修复成功时保持静默，不逐项汇报；网络、权限、fetch、初始化或复检失败时应停止依赖该环境的操作并说明实际阻塞，不得把失败当作通过。保留平台注入的代理、凭据和 CA 配置，不输出密钥。

# DeepSeek 调用规则

- 调用 DeepSeek 默认且仅使用 `deepseek-flash`，通过 `tools/deepseek.py` 调用。
- 未经用户明确授权，不得调用其他 DeepSeek 模型，也不得使用 `deepseek-chat`、`deepseek-reasoner` 等别名。
- 只有用户明确授权了其他模型及其使用范围后，才能在该范围内使用 `--model` 和 `--allow-other-model`；不得自行添加放行参数。
- Flash 出错、不可用或效果不足时，不得自动切换模型。需要其他模型时，先向用户申请授权。
- 不得通过直接 API 请求、其他脚本或修改默认值绕过上述规则。
- 创建这些规则的授权仅允许编辑文件，不代表授权调用其他模型。
- 仅发送任务所需内容，不发送密钥或无关工作区文件。
