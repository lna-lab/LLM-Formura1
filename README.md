# 🏁 LLM Formula

### The World Championship of Inference Efficiency

> # 🔥 Don't burn cash with your tokens — burn passion.
> ### *« Brûlez la passion, pas les billets. »*
> <sub>The championship motto, in the language of the FIA.</sub>

*The privateer's creed: you don't win by buying the biggest cluster. You win by engineering the cleverest joule.*

> **FLOPs are free. The only fight is bandwidth, latency, and joules.**

*Issued by **Lna-Lab** · Season 1 (2026) · Charter date: 2026‑05‑29*

---

## What this is

**LLM Formula** is an open, global motorsport-style championship for **large-language-model inference**. Competitors — from lone privateers with a pair of consumer GPUs to works teams with server racks — race the *same homologated model* and are scored on how well they convert **electricity into tokens**.

Modern Formula 1 is not a contest of raw horsepower; since the hybrid era it is an **energy-efficiency formula** — a fixed fuel allowance, and victory to whoever converts it most cleverly into speed. **LLM Formula applies the same spirit to AI inference.** The headline metric is **tokens-per-joule**. The craft is in the tune: quantization, batching, kernel fusion, clock/voltage control, parallel topology, speculative decoding.

You do not need the biggest cluster. You need the best engineering.

---

## The Championships

| Title | Metric | Character |
|---|---|---|
| 🏆 **Pace** (Fastest Lap) | peak single-stream tokens/s | the qualifying lap — latency craft |
| 🏆 **Efficiency** (the blue riband) | **tokens / joule** (wall energy) | the hybrid fuel formula — true engineering |
| 🏆 **Endurance** (Constructors') | aggregate tokens/s under the power cap | Le Mans — throughput under a fuel limit |

## The Classes — a power formula

Classes are defined by **sustained wall power** (the true whole‑system AC draw — see [MEASUREMENT.md](MEASUREMENT.md)) — our equivalent of the fuel‑flow regulation. There is **no unlimited / works‑only class**: by design every class is runnable by **an individual, in any country, from a single domestic mains outlet.** The World Champion may live in a bedroom, not a datacenter. **Apple Silicon, AMD, Jetson and CPU rigs are first‑class** — there is no interconnect or vendor restriction; only watts and correctness are regulated.

| Class | Power cap | Who |
|---|---|---|
| **GP1000 — Grand Prix** | ≤ 1 000 W | The iconic halo class. The open big‑power flagship; the place to chase the future **1000 TPS** single‑stream era. |
| **GP400 — the grid** | ≤ 400 W | The practical heart of the series: a Mac Studio, a single big card (e.g. 96 GB workstation), a power‑capped multi‑GPU rig. Where most privateers actually race. |
| **E50 — Edge** | ≤ 50 W | Laptops, Apple Silicon on battery, Jetson, power‑capped single accelerators. The eco extreme. |

> **Why the "1000"?** It is a double meaning. 1000 W is a power any household circuit can deliver **anywhere** (even Japan's 100 V/15 A). And **1000 also looks ahead to the 1000‑TPS single‑stream era** we are driving toward — the iconic number the flagship is named for. Most racing happens in **GP400** and **E50**; GP1000 is the glamour at the top.
>
> **GP400 exists so no single product owns a class** — a 300 W workstation card competes there, but with 100 W of company (Macs, dual small GPUs), so it never becomes a one‑make series.
>
> Reference rig **DwarfStar4** (7× RTX PRO 2000 Blackwell, ~490 W board) races in **GP1000**.

---

## How to enter

1. Read the **[Regulations](REGULATIONS.md)** — the technical & sporting rulebook.
2. Run a **homologated engine** (spec model) on your hardware.
3. Pass **scrutineering**: your output must match the reference within tolerance — *you cannot win by breaking the model.* **Correctness before speed.**
4. Submit a **result manifest** (see **[ENTRY.md](ENTRY.md)**): hardware, model checksum, energy trace, token count, wall time, output hash.
5. A steward independently reproduces your run. Verified times go on the **leaderboard**.

Privateers welcome. Open source encouraged. Glory to the cleverest joule.

---

## Call for Partners & Sponsors

LLM Formula is a stage for **sustainable, efficient AI** and for the engineers who build it. We invite:

- **GPU / accelerator vendors**, **PSU / cooling / power** makers, **cloud & datacenter** providers — as **Technical Partners**.
- **Title & Series sponsors** who want their name on the championship of AI efficiency.
- A **Privateer Support Fund** — hardware grants so a brilliant tuner anywhere on Earth can enter.

See **[PARTNERS.md](PARTNERS.md)**. Reach the people optimizing the future of inference, measured — not marketed.

---

## Repository

| | |
|---|---|
| 📕 [REGULATIONS.md](REGULATIONS.md) | Sporting & technical rulebook (v1.1‑draft) |
| 🌍 [HOMOLOGATION.md](HOMOLOGATION.md) | The constructors' grid — the world's open‑weight engines by class & nation |
| 📐 [MEASUREMENT.md](MEASUREMENT.md) | The binding measurement standard (Energy‑of‑Record, tiers, reproduction) |
| ⚙️ [BULLETIN-1.md](BULLETIN-1.md) | The adversarial integrity review that hardened v1.0 → v1.1 |
| 🏁 [ENTRY.md](ENTRY.md) | How to compete + result‑manifest schema |
| 🤝 [PARTNERS.md](PARTNERS.md) | Technical partners, sponsors, privateer support fund |
| 🔧 [tools/llmf-bench/](tools/llmf-bench/) | The one‑command measurement harness (OpenAI‑compatible) |
| 📊 [tools/build_site.py](tools/build_site.py) → `site/` | Static leaderboard generator ([DEPLOY.md](DEPLOY.md)) |
| 📁 [results/](results/) | Result manifests → the leaderboard |

## Status

- **Season 1 (2026)** — charter & regulations published 2026‑05‑29, then **hardened by an independent adversarial review** ([BULLETIN-1.md](BULLETIN-1.md)): v1.0 was found gameable and rebuilt to v1.1. Integrity‑first rollout — rules + measurement standard now; provisional Round 1 shakedown next.
- Founder & Series Director: **Tonoken3 / Lna‑Lab**.
- Technical supervision & measurement methodology: **Claude Opus 4.8** (the reference scrutineering harness is built on the open **DwarfStar4** engine).

Regulations & docs are offered openly to the world (CC BY 4.0). Fork them, run a round, start a national series. The grid is open.

> 🏁 *Let the World Grand Prix begin.*
