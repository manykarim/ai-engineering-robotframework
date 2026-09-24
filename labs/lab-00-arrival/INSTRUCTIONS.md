# Lab 0 - Arrival

Get your own copy of the workshop running: the repository, the shop, the test suite and your coding agent.
Everything later builds on this.

| | |
|---|---|
| Module | 0 - Arrival & Environment Check |
| Time | 30 minutes |
| Shop preset | `clean` |
| You need | The prerequisites of [SETUP.md](../../SETUP.md#prerequisites), a GitHub account, and your coding agent installed and signed in |
| You start from | Nothing: this lab creates your copy |

Stuck on a step? Say so in the chat. The co-host runs a breakout room for exactly this.

## Steps

1. **Fork** the repository on GitHub with the *Fork* button. Keep the name. Lab 9 runs on your fork, and you take
   everything you build today home in it.

2. **Clone your fork** and enter it:

   ```bash
   git clone https://github.com/<your-handle>/ai-engineering-robotframework.git
   cd ai-engineering-robotframework
   ```

3. **Install** the pinned environment and its browser:

   ```bash
   uv sync --locked
   uv run --no-sync rfbrowser install chromium
   ```

4. **Start the shop.** Pick one:

   - *With Docker*, run the [local shop](../../SETUP.md#the-local-shop):

     ```bash
     docker compose -f shop/compose.yaml up -d
     ```

   - *Without Docker*, use your own [space](../../GLOSSARY.md#space) on the [shared instance](../../SETUP.md#the-shared-instance). Create
     a file `.env` in the repository root with the address the facilitator gave you and your GitHub handle:

     ```bash
     SHOP_URL=https://<shared instance>
     SHOP_SPACE=<your-github-handle>
     ```

5. **Check everything** in one go:

   ```bash
   uv run --no-sync python setup-check/check.py
   ```

   Every line should be green. Yellow warnings about optional tools (Azure CLI, Jira) are fine. For anything red,
   the check prints the fix.

6. **Look at the shop** in your browser: `http://localhost:9090`, or the shared address. It is a small web shop
   with a catalogue, a cart and a checkout. The test suite and all your labs work against it.

7. **Ask the shop what state it is in:**

   ```bash
   uv run --no-sync python -m shop status
   ```

   It shows the shop's version, your space if you have one, and the [presets](../../GLOSSARY.md#preset) that hold.
   It should say `clean`.

8. **Run the test suite once:**

   | Local shop | Shared instance |
   |---|---|
   | `uv run robotcode robot` | `uv run robotcode -p shared robot` |

   It runs 13 tests in about a minute.

9. **Read the result** the way your agent will later:

   ```bash
   uv run robotcode results summary
   uv run robotcode results show --failed
   ```

   11 tests pass and 2 fail. Both failing tests carry the tag `broken`: they fail on purpose, and you will meet them
   again in Modules 4 and 5. Everything else is green.

10. **Start your coding agent** in the repository root (`claude`, `codex` or `copilot`) and give it this prompt:

    > What is this repository, and how do I run its tests?

    It answers from `AGENTS.md`, the short context file every agent reads. Lab 2 builds it out.

## Stretch

- List the presets the shop knows: `uv run --no-sync python -m shop presets`. Which ones sound like they break
  something? Don't apply any yet: every lab tells you when.
- Open `tests/ui/catalogue.robot` and `resources/catalogue.resource`. Which file holds the locators?

## If your agent fails

Everything up to step 9 needs no agent. If yours won't start or sign in, tell the co-host, and follow
[the recorded walkthrough of this lab](../../transcripts/lab-00-arrival.md) for step 10.
