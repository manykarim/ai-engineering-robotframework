# Environment

- Install: `uv sync --locked`, then `uv run --no-sync rfbrowser install chromium`.
- Check the environment: `uv run --no-sync python setup-check/check.py`.
- Run the suite: `uv run robotcode robot`. Plain `robot` ignores `robot.toml` and cannot find the shop.
- Run one test: `uv run robotcode robot -t "<test name>"`.
- `-p shared` selects the shared instance: `uv run robotcode -p shared robot`. Without it, the local shop.
- Logs and reports go to `results/`, which git ignores.
