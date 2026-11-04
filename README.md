# dsh-learn

用于学习和体验 DeepSeek Harness 与 dsh-superagent 的测试仓库。

## Server status tool

`server-status` reports CPU, memory, and disk usage for the local host.

### Install

Python 3.9 or newer is required. From the repository root:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

### Use

Print a readable report:

```bash
server-status
```

Print machine-readable JSON:

```bash
server-status --json
```

The tool reads the host where it runs. It does not connect to remote servers or change running services.

### Test

```bash
python -m unittest discover -s tests -v
```
