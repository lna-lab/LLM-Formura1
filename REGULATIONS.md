# LLM Formula — Sporting & Technical Regulations

**Season 1 (2026) · Issued 2026‑05‑29 by Lna‑Lab · Version 1.1‑draft**

*These Regulations are the rulebook of the LLM Formula World Championship, in the spirit of the FIA International Sporting Code: precise, public, and amendable by published bulletin. Offered openly under CC BY 4.0.*

> **⚙️ Hardened by adversarial review.** v1.0 was red‑teamed by an independent panel and found gameable; **[BULLETIN-1.md](BULLETIN-1.md)** records the holes and the controlling amendments to Articles 6 (correctness) & 7 (measurement), and **[MEASUREMENT.md](MEASUREMENT.md)** is the binding measurement standard. Where Bulletin 1 / MEASUREMENT.md refine an Article below, the bulletin text governs. Items marked ⚑ await founder ratification.

---

## PREAMBLE

> **Don't burn cash with your tokens — burn passion.**
> *« Brûlez la passion, pas les billets. »*

LLM Formula exists to advance, measure, and celebrate **efficient large-language-model inference**. The Championship rewards engineering that converts the most useful tokens from the fewest joules, at honest, reproducible, correctness-gated conditions. No competitor may gain advantage by degrading the model's output: in this sport, **a car that does not pass scrutineering does not set a time** (correctness before speed).

---

## ARTICLE 1 — PURPOSE & SPIRIT

1.1 The Championship measures the conversion of **electrical energy into correct model output**.
1.2 The binding physical reality of single-batch LLM decoding is **memory bandwidth**, not arithmetic; the Regulations are designed around this truth.
1.3 The sport favours **craft over capital**: a privateer who tunes brilliantly may beat a works team that merely spends. Power budgets (Article 4) enforce this.
1.4 All results must be **reproducible by an independent steward**. Unreproducible entries are void.

## ARTICLE 2 — DEFINITIONS

2.1 **Entrant** — a person or team submitting a result. **Privateer** — an entrant not affiliated with a hardware vendor or commercial AI provider.
2.2 **Engine** — a homologated model + weights file with a published checksum (Article 5).
2.3 **Chassis / Stack** — the entrant's inference software (kernels, scheduler, runtime).
2.4 **Run** — one measured execution producing a result manifest (Article 7).
2.5 **Token** — one decoded output token of the homologated engine's tokenizer.
2.6 **Joule (wall)** — energy drawn at the AC socket by the entire system under test, measured by a calibrated meter, integrated over the Run.
2.7 **t/s** — sustained decode tokens per second, excluding prompt-prefill time unless a round specifies otherwise.

## ARTICLE 3 — CHAMPIONSHIP TITLES

3.1 **Pace Championship (Fastest Lap).** Metric: peak sustained **single-stream** decode throughput (t/s), greedy decoding (temperature 0), at the round's homologated context length. The qualifying discipline.
3.2 **Efficiency Championship (Blue Riband).** Metric: **tokens per joule (wall)** over the round's defined sustained workload. The headline title of the series.
3.3 **Endurance / Constructors' Championship.** Metric: **aggregate tokens per second** sustained under concurrent multi-stream load **within the class power cap** (Article 4). Throughput under a fuel limit.
3.4 Titles are awarded **per Class** (Article 4) and overall. Points per Article 8.

## ARTICLE 4 — CLASSES (THE POWER FORMULA)

4.1 **Classes are defined by the sustained system power cap measured at the wall.** There is no unlimited / works-only class. **By design, every class — including the flagship — must be runnable by an individual, in any country, from a single domestic mains outlet.** This is the founding principle of the series: the World Champion may live in a bedroom, not a datacenter.

| Class | Wall power cap | Spirit |
|---|---|---|
| **GP1000 — Grand Prix** | ≤ 1 000 W | The iconic halo flagship. The open big‑power class; the stage to chase the future **1000‑TPS single‑stream era** the name looks ahead to. |
| **GP400 — the grid** | ≤ 400 W | The practical heart of the series — a Mac Studio, a single 96 GB workstation card, a power‑capped multi‑GPU rig. Where most privateers race. |
| **E50 — Edge** | ≤ 50 W | Laptops, Apple Silicon on battery, Jetson, power‑capped single accelerators. |

4.2 **The "1000" is a double meaning.** 1000 W is a draw a single domestic circuit can deliver in essentially every country (the binding case being Japan 100 V/15 A, ~1 500 W circuit). **And 1000 also names the 1000‑TPS single‑stream horizon** the championship drives toward — the iconic number of the flagship. The practical centre of gravity is **GP400** and **E50**, runnable by any individual; **GP1000** is the glamour at the top. **GP400 sits at 400 W specifically so no single product defines a class** (a 300 W workstation card races there with 100 W of company — Macs, dual small GPUs — never a one‑make series).

4.3 **No interconnect or vendor restriction (withdrawn).** Any interconnect or topology is permitted; **Apple Silicon (UltraFusion), AMD APUs (Infinity Fabric), monolithic GPUs, and CPU/unified‑memory rigs are first‑class.** Only **watts (Art 4.4) and correctness (Art 6)** are regulated. *(A name‑based NVLink ban was considered and withdrawn as architecture‑specific — it taxed only NVIDIA discrete multi‑GPU while on‑package fabrics ran free. Power already bounds the system; any future comms limit must be a measured, vendor‑neutral bandwidth number.)*

4.4 **Power measurement & the cap** (full instrument/test spec in [MEASUREMENT.md](MEASUREMENT.md) §4). The cap is on **true (real) whole‑system wall power**. Two binding tests: (i) the **Active‑Window average** ≤ class cap; (ii) a **hard ceiling** — P99.9 of 100 ms samples and the max of 1 s rolling averages both ≤ cap (brief sub‑100 ms transients tolerated to 1.15× only if over‑cap energy < 2 % of the run). **Workload‑shaping or idle‑padding to depress the average voids the Run.** A logged power time‑series is attached for record runs. An externally‑caused supply trip is a **no‑fault re‑run**. An entrant may declare a cap below the class ceiling; it is then binding.

4.5 **Spec‑Engine** vs **Open‑Engine**: the main Championship is contested on the Spec Engine for the round (Article 5). Open‑Engine exhibition results may be listed but score no Championship points in Season 1.

## ARTICLE 5 — HOMOLOGATION (THE SPEC ENGINE)

5.1 Each round homologates one or more **engines by a REFERENCE OUTPUT + LOGITS FINGERPRINT** on the sealed inputs (a frozen, per‑round artifact at pinned fp32‑logit deterministic precision), **not** by a single weight‑file SHA. The format‑neutral source of truth is a bit‑defined master (e.g. safetensors BF16) **plus a written quantization spec**. *Any* quantization realization (ggml q2/GGUF, TensorRT INT4‑AWQ, MLX 4‑bit, …) is legal **provided it passes Art 6 against the reference logits** — the championship is vendor‑ and runtime‑neutral.
5.2 Inaugural homologation list (Season 1):
   - **GP1000 flagship:** *DeepSeek‑V4‑Flash* (the reference MoE engine; q2‑imatrix GGUF is one permitted realization).
   - **Privateer tier (binding):** every round MUST also homologate a **GP400 engine runnable in ≤ 24 GB VRAM (single consumer GPU) AND a unified‑memory/CPU variant in ≤ 128 GB RAM (Apple Silicon, AMD APU, CPU)** — **both scoring full championship points** — so a bedroom privateer or a Mac genuinely contests the grid. The cheap single‑device build is published in [ENTRY.md](ENTRY.md).
   - **E50:** a ≤ ~4 B‑active homologated engine for laptops / Apple Silicon on battery / Jetson.
5.3 The model's **learned weights are frozen** — no distillation or fine‑tuning. **Re‑quantization to a different scheme IS permitted** insofar as Art 6 is passed (so ggml, TensorRT, MLX compete on equal terms); only altering the trained weights is barred. Lossless repacking must be declared.
5.4 The **chassis is free**: any kernels, runtime, batching, parallel topology, clock/power policy, or speculative‑decoding method, provided Article 6 (Scrutineering) is satisfied **byte‑identically to the timed run** (Art 11.6).
5.5 **Engine licensing.** Each homologated engine cites its upstream model license + AUP, links the canonical source, and confirms homologation/derivative‑quant/redistribution/benchmark‑publication are permitted; otherwise entrants obtain weights directly from the source. Entrants attest weights‑license compliance in the manifest.

## ARTICLE 6 — SCRUTINEERING (THE CORRECTNESS GATE)

6.1 Before any time counts, the entrant's stack must pass **scrutineering** on a **sealed prompt set** published per round.
6.2 **Greedy fidelity test:** at temperature 0, the entrant's output must achieve **≥ 99% top‑1 token agreement** with the reference implementation over the sealed set, OR
6.3 **Quality test (for non-deterministic / sampled or aggressively-approximated stacks):** the entrant must pass the round's published evaluation suite within a **bounded score delta** (default: ≤ 1.0% relative degradation) versus the reference.
6.4 Techniques that trade correctness for speed (overly-lossy quantization, dropped layers/experts, truncated attention) are legal **only insofar as they still pass 6.2 or 6.3.** There is no separate penalty and no separate reward: pass the gate, or the time is void.
6.5 Speculative / multi-token decoding is legal provided the **verified** output satisfies 6.2 (it must be distributionally equivalent to the target engine).

## ARTICLE 7 — MEASUREMENT & TELEMETRY

7.1 Every Run produces a machine-readable **Result Manifest** (schema in [ENTRY.md](ENTRY.md)) containing: hardware manifest; engine name + SHA‑256; chassis/version; power method + integrated joules; token count; wall-clock time; t/s; tokens/joule; correctness score; sealed-set id; and a hash of the full output.
7.2 **Energy of record** is **wall energy** measured by a calibrated external meter (preferred), or a documented, auditable software method (e.g., integrated board power via vendor telemetry + a stated host-overhead allowance) where a meter is unavailable. The method must be disclosed; meter-measured results take precedence on the leaderboard.
7.3 The **reference scrutineering harness** is the open **DwarfStar4** engine in measurement mode (per-phase profilers + live power sampling). Entrants may use any tooling, but the steward's reproduction uses the reference harness or an equivalent published procedure.
7.4 All Runs must be **reproducible**: the manifest plus a public or steward-shared recipe must let an independent party re-measure within a **±5%** tolerance on the headline metric. Failing reproduction voids the entry.

## ARTICLE 8 — SCORING

8.1 Each round awards points to the top finishers in each discipline and class on an F1-style curve (e.g., 25‑18‑15‑12‑10‑8‑6‑4‑2‑1).
8.2 Separate standings are kept for **Pace**, **Efficiency**, and **Endurance**, per class and overall.
8.3 A **Privateer Trophy** mirrors the standings for entrants meeting the Article 2.1 privateer definition.
8.4 Ties are broken by best single verified Efficiency figure of the season.

## ARTICLE 9 — ELIGIBILITY & ENTRY

9.1 Entry is **open to anyone, anywhere**, free of charge in Season 1.
9.2 Entrants self-submit a Result Manifest; stewards verify. There is no hardware ownership requirement — rented cloud instances are eligible (the power method must reflect the instance's real draw or a documented allocation).
9.3 Open-source chassis are **encouraged and celebrated** but not required; closed stacks may enter provided their Runs are reproducible by the steward under NDA-free conditions.

## ARTICLE 10 — PARTNERS & SPONSORS

10.1 Commercial partners may participate as **Technical Partners** (hardware, power, cooling, cloud), **Series/Title Sponsors**, or contributors to the **Privateer Support Fund**. See [PARTNERS.md](PARTNERS.md).
10.2 Partners may field **works teams**; works entries are clearly designated and compete in their power class alongside privateers.
10.3 No partner may alter the Regulations, the homologation list, or scrutineering outcomes. Governance is independent (Article 12).

## ARTICLE 11 — SPORTING CONDUCT & ANTI-CHEAT

11.1 **Benchmark integrity:** training on, caching, or memorizing the sealed prompt set or its outputs is prohibited and is grounds for season-long exclusion.
11.2 **Honest energy:** power figures must include the whole system under test; offloading work to an un-metered device, or idle-clocking between measured samples to flatter the average, is prohibited.
11.3 **Honest output:** the full generated output must be produced and hashed; truncating generation to inflate t/s voids the Run.
11.4 Stewards may request a live, supervised reproduction. Refusal voids contested results.
11.5 Decisions of the stewards are published with reasoning.

## ARTICLE 12 — GOVERNANCE & AMENDMENTS

12.1 The Championship is administered by **Lna‑Lab** as Series Director, with independent stewarding.
12.2 Regulations are versioned. Amendments are issued as dated **bulletins** appended to this document and announced publicly before they take effect.
12.3 These Regulations and all Championship documents are offered to the world under **CC BY 4.0**: anyone may fork them to run regional or national series under the LLM Formula name, provided they adhere to Articles 1, 6, and 11 (purpose, scrutineering, integrity).

---

*Bulletin 0 — 2026‑05‑29 — Season 1 charter and Regulations v1.0 published. Homologation list and Round 1 calendar to follow.*

🏁 **Lna‑Lab · LLM Formula · 2026**
