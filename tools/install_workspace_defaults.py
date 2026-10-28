#!/usr/bin/env python3
"""Install the repository's DeepSeek defaults across /workspace."""

from pathlib import Path
import shutil


def main():
    source = Path(__file__).resolve().parent
    workspace = Path('/workspace')
    target = workspace / 'tools' / 'deepseek.py'
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.resolve() != (source / 'deepseek.py').resolve():
        shutil.copyfile(source / 'deepseek.py', target)

    start = '<!-- BEGIN DEEPSEEK DEFAULTS -->'
    end = '<!-- END DEEPSEEK DEFAULTS -->'
    block = f'''{start}
## DeepSeek 工作区规则

- 本工作区所有项目调用 DeepSeek，统一使用 `/workspace/tools/deepseek.py`。
- 默认模型仅为 `deepseek-flash`，默认输出上限为 `16384` tokens。
- 未经用户明确授权，不得使用其他模型或别名，不得添加 `--allow-other-model`。
- 只有用户明确授权了其他模型及其使用范围后，才可在该范围内显式放行。
- 不得通过其他脚本、直接 API 请求或修改配置绕过模型限制；失败时不得自动切换模型。
- 仅发送任务所需内容，不发送密钥或无关文件。
{end}'''
    instructions = workspace / 'AGENTS.md'
    existing = instructions.read_text() if instructions.exists() else ''
    if start in existing:
        before, rest = existing.split(start, 1)
        if end not in rest:
            raise ValueError('Incomplete DeepSeek instructions block; repair it before installing')
        _, after = rest.split(end, 1)
        updated = before + block + after
    else:
        updated = existing.rstrip() + '\n\n' + block + '\n'
    instructions.write_text(updated.lstrip('\n'))
    print(f'Installed {target} and workspace instructions in {instructions}')
    print('Defaults: deepseek-flash, max_tokens=16384. Rerun after environment rebuilds or helper updates.')


if __name__ == '__main__':
    main()
