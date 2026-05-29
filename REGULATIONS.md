# LLM Formula — Sporting & Technical Regulations

**Season 1 (2026) · Issued 2026‑05‑29 by Lna‑Lab · Version 1.0**

*These Regulations are the rulebook of the LLM Formula World Championship. They are written in the spirit of the FIA International Sporting Code: precise, public, and amendable by published bulletin. Offered openly under CC BY 4.0.*

---

## PREAMBLE / 序文

> **「お前のトークンで札束を燃やすな。情熱を燃やせ。」 — Don't burn cash with your tokens; burn passion.**

LLM Formula exists to advance, measure, and celebrate **efficient large-language-model inference**. The Championship rewards engineering that converts the most useful tokens from the fewest joules, at honest, reproducible, correctness-gated conditions. No competitor may gain advantage by degrading the model's output: in this sport, **a car that does not pass scrutineering does not set a time**（正答性 > 速度）.

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

| Class | Wall power cap | Interconnect rule | Spirit |
|---|---|---|---|
| **GP1000 — Grand Prix** | ≤ 1 000 W | **PCIe-only** (no NVLink/NVSwitch/proprietary fabric) | The flagship. 1 kW fits a single domestic circuit **anywhere on Earth** (e.g. Japan 100 V/15 A, US 120 V/15 A, EU 230 V) — so the top class is open to every individual, not just server rooms. |
| **GT300** | ≤ 300 W | **PCIe-only** | The efficiency midfield — a single prosumer GPU or a power-capped multi-GPU rig. |
| **E50 — Edge** | ≤ 50 W | single-node (on-package / PCIe) | Laptops, Apple Silicon, Jetson, power-capped single accelerators. The eco extreme. |

4.2 **Why 1 000 W is the ceiling.** A continuous ~1 kW draw is within a single household outlet/circuit in essentially every country (the binding case being 100 V/15 A Japan, ~1 500 W circuit, comfortably clearing 1 kW). Capping the top class here guarantees the Championship is **globally accessible to private individuals** and keeps the contest about engineering, not electrical-service privilege.

4.3 **Interconnect restriction (GP1000 & GT300).** Links faster than PCIe between accelerators — NVLink, NVSwitch, or any proprietary high-bandwidth fabric — are **prohibited** in these classes. Competition rides on consumer/prosumer interconnect, so all-reduce/all-to-all bandwidth is a shared, level constraint (the reference rig is itself PCIe-only). E50 is effectively single-node and the rule is moot.

4.4 **Power measurement.** The cap is the sustained wall power **averaged over the Run**; exceeding it at any 1-second sample by >5% is a black flag for that Run. An entrant may declare a cap **below** their class ceiling to contest Efficiency at a chosen operating point; the declared cap is then binding for that Run.

4.5 **Spec-Engine** vs **Open-Engine**: the main Championship is contested on the Spec Engine for the round (Article 5). Open-Engine exhibition results may be listed but score no Championship points in Season 1.

## ARTICLE 5 — HOMOLOGATION (THE SPEC ENGINE)

5.1 Each round names one or more **homologated engines** (model + exact weights file) with a published **SHA‑256 checksum**, tokenizer, and reference decoding configuration.
5.2 Inaugural homologation list (Season 1):
   - **GP1000 flagship:** *DeepSeek‑V4‑Flash* (q2‑imatrix GGUF) — the reference MoE engine.
   - **GT300 / E50:** lightweight homologated engines (e.g. ≤ ~4 B active) to be named on the homologation bulletin, so single-GPU, Apple-Silicon, and edge privateers can race.
5.3 The model weights are **frozen**. Re-quantization, distillation, or fine-tuning of the homologated weights is **not** permitted in the Spec-Engine Championship (it changes the engine). Lossless repacking that preserves bit-exact dequantized weights is permitted and must be declared.
5.4 The **chassis is free**: any kernels, runtime, batching scheme, parallel topology, clock/power policy, or speculative-decoding method may be used, provided Article 6 (Scrutineering) is satisfied.

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
