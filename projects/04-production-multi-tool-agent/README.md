# Production Multi-Tool Agent

A small production-shaped agent that routes a request to calculator, local search, and weather tools, isolates tool failures, aggregates results, and records orchestration timing.

## Run

```powershell
uv run python main.py "Explain RAG and calculate: 6 * 7"
uv run python main.py "What is the weather in Tokyo?"
```

The demo uses local data so it runs without API keys. Replace the tool implementations with provider clients when connecting external services.

## Structure

- `tools/`: isolated tool implementations
- `agent/router.py`: deterministic request routing
- `agent/orchestrator.py`: tool execution and error isolation
- `agent/aggregator.py`: final response formatting
- `observability/tracing.py`: timing instrumentation
