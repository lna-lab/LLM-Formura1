# llmf-bench — LLM Formula reference measurement harness

One self-contained Python script (stdlib only) that benchmarks an **OpenAI-compatible
endpoint**, measures energy over the **Active Window**, scores the greedy **correctness
gate**, and emits an `llmf-result/2` manifest. Runs anywhere: NVIDIA / AMD / Apple
Silicon / CPU / cloud. See [../../MEASUREMENT.md](../../MEASUREMENT.md) and
[../../REGULATIONS.md](../../REGULATIONS.md) Art. 6–7.

## Requirements
Python 3.8+. No pip installs. Your engine must expose an OpenAI-compatible
`/v1/completions` (or `/v1/chat/completions` with `--chat`) — e.g. `ds4-server`,
vLLM, llama.cpp server, LM Studio, MLX-server, TGI.

## Quick start (the honest, scoring path — external wall meter)
1. Plug your **whole rig** into a wall energy meter / smart plug that logs `unix_ts,watts`
   at ≥1 Hz (the meter must enclose the entire System Under Test — every device doing
   inference work). Save it as `watts.csv` while the run executes.
2. Get the round's sealed practice set (`round1_practice.jsonl`) — or try the bundled
   `example_reference.jsonl`.
3. Run:
```bash
python3 llmf_bench.py run \
  --endpoint http://localhost:8080/v1 --model deepseek-v4-flash \
  --reference example_reference.jsonl \
  --class GP400 --round 1 --discipline efficiency \
  --handle your-handle --chassis "my-stack v1.2" \
  --meter external-csv --meter-csv watts.csv --idle-watts 12.0 \
  --max-tokens 256 --out result.json
```
4. Submit `result.json` (PR to `results/<season>/<class>/<handle>.json`, or the web form).
   A steward reproduces it (median of 3) on a **held-out** slice — that is the official figure.

## Meters & tiers (MEASUREMENT.md §5)
| `--meter` | sensor_class | Scores? |
|---|---|---|
| `external-csv` (a real wall meter) | external | ✅ yes (Tier A/B) |
| `nvidia-smi` (firmware telemetry) | firmware | exhibition only (0 pts) |
| `manual` (`--avg-watts`) | manual | exhibition only |

Only an **external whole-system meter** scores. Firmware board power and self-declared
averages are exhibition — they under-count real draw and can't be trusted for a title.

## Apple Silicon / laptops / cloud
Macs and laptops have no DC rails — that's exactly why the Energy-of-Record is **AC-wall**.
Use a wall smart-plug (`external-csv`). Single-tenant whole-node cloud: use PDU/Redfish
energy exported to the same CSV format.

## What the gate checks (client side)
Greedy **exact-match rate** vs the reference output, plus **critical-span** match
(final answer / label) when the reference provides `answer_span`. The full teacher-forced
top-1 + logit + distributional gates (Art. 6) run **steward-side** with reference logits.

## reference jsonl format
```json
{"id": "q1", "prompt": "What is the capital of France?", "reference": "The capital of France is Paris.", "answer_span": "Paris"}
```

> ⚠️ Self-reported numbers are provisional. The leaderboard figure of record is the
> steward's median-of-3 on the sealed hold-out. Correctness before speed.
