
- https://github.com/astral-sh/uv

## Install uv

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Create virtual environment
```bash
uv venv  --python=python3.10 ~/py3.10
```

## Activate virtual environment
```bash
source $HOME/py3.10/bin/activate
uv pip install torch ipython
```


