# How to Enter — LLM Formula

**Season 1 (2026) · 2026‑05‑29**

A run only counts when it is **correct, metered, and reproducible**. Here is the whole procedure.

## 1. Pick a class and engine
- Choose your **Class** by your sustained wall-power budget: **GP1000** (≤1 000 W, PCIe-only), **GT300** (≤300 W, PCIe-only), **E50** (≤50 W). No unlimited class — the flagship runs on one domestic outlet anywhere. See [REGULATIONS](REGULATIONS.md) Art. 4.
- Run the round's **homologated engine** (model + exact weights, by SHA‑256). See Art. 5.

## 2. Build your stack (the chassis is free)
Tune anything: kernels, quantized matmul, **batching / continuous batching**, parallel topology (TP/PP/EP/DP), **clock & power policy** (DVFS), **speculative / multi-token decoding**. The only rule is the correctness gate below.

## 3. Pass scrutineering (correctness gate — Art. 6)
On the round's **sealed prompt set**, at temperature 0, achieve **≥ 99% top‑1 token agreement** with the reference — or pass the round's eval suite within **≤ 1.0%** degradation. *No time counts until you pass.* 正答性 > 速度.

## 4. Measure (Art. 7)
- **Energy of record = wall joules** from a calibrated meter (preferred). If no meter, document an auditable software method (e.g., integrated board power + stated host overhead); meter results outrank software results.
- Record token count, wall time, t/s, tokens/joule, and a **hash of the full output**.

## 5. Submit a Result Manifest
Open a Pull Request adding `results/<season>/<class>/<your-handle>.json`, or open an Issue with the manifest. A steward will independently reproduce it (±5% tolerance) before it joins the leaderboard.

### Result Manifest schema (v1)

```json
{
  "schema": "llmf-result/1",
  "season": 2026,
  "round": 1,
  "discipline": "efficiency",            // "pace" | "efficiency" | "endurance"
  "class": "GP1000",                      // "GP1000" | "GT300" | "E50"
  "entrant": { "handle": "lna-lab", "privateer": true, "team": null },
  "engine": {
    "name": "DeepSeek-V4-Flash",
    "weights_sha256": "<hex>",
    "tokenizer": "<id-or-sha>",
    "lossless_repack": false
  },
  "chassis": { "name": "DwarfStar4", "version": "git:5dd80d1", "open_source": true },
  "hardware": {
    "gpus": "7x NVIDIA RTX PRO 2000 Blackwell 16GB",
    "interconnect": "PCIe5 (no NVLink)",
    "host": "AMD EPYC 48-core, 1TB RAM",
    "notes": ""
  },
  "workload": {
    "context_len": 512,
    "concurrency": 1,                     // >1 for endurance
    "temperature": 0,
    "sealed_set_id": "<published-per-round>"
  },
  "measurement": {
    "energy_method": "wall-meter",        // "wall-meter" | "software-board+overhead"
    "meter": "<model/calibration>",
    "tokens": 12000,
    "wall_seconds": 644.0,
    "joules_wall": 106560.0,
    "avg_system_watts": 165.5
  },
  "results": {
    "tokens_per_second": 18.63,
    "tokens_per_joule": 0.1126,
    "correctness_top1_agreement": 0.997
  },
  "output_sha256": "<hex of full concatenated output>",
  "reproduction": { "recipe_url": "<public steps or repo>", "steward_verified": false }
}
```

## 6. Get verified → hit the leaderboard
The steward reproduces, signs the manifest (`steward_verified: true`), and your time is official. Season standings follow [REGULATIONS](REGULATIONS.md) Art. 8.

> Privateers, students, garage tuners — you are the heart of this series. Bring your cleverest joule. 🏁
