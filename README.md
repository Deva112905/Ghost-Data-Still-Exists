# Deletion audit agent

Pipeline: `loader` -> `gate` (NOT_APPLICABLE) -> `discover` (identity, state, rules, flows, restores) -> `planner` (status + steps) -> `ordering` -> `writer`.
Everything that decides ordering and step content is deterministic. The LLM (`audit/llm.py`) is meant only for evidence code cannot parse, with caching and usage logging.

## Run
    python tests/test_planner.py                 # planner/ordering tests
    python run.py --dry-run                      # applies only the NOT_APPLICABLE gate
    python run.py                                # writes output.csv (needs audit/discover.py implemented)
    python evaluation/evaluate.py predicted.csv dataset/sample_output.csv

Put the competition `dataset/` folder next to `run.py`. Set `ANTHROPIC_API_KEY` in the environment if you use the LLM; never commit keys.

## Status
Done and tested: step ordering, planner, output writer (518-row check), evaluator, usage report, extra cases.
NOT done: `audit/discover.py` (reads the real schemas) and tuning `audit/gate.py` and `verify_all_in_incomplete` against `sample_output.csv`.
