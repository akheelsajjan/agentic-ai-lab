 # Project 07: Multi-Agent Research

This project uses a LangGraph workflow to produce a structured research report from several specialized agents.

```text
Research -> Technical Analysis -> Industry Analysis -> Critic -> Writer
```

## Run

Set `GROQ_API_KEY` in the environment or in a `.env` file, then run:

```bash
uv run python main.py "How are AI coding agents changing software development?"
```

Set `GROQ_MODEL` to override the default Groq model.
