# Bulletin 1 — Integrity Review & Regulations v1.1

**2026‑05‑29 · Lna‑Lab · supersedes v1.0 where in conflict**

Before opening a grid, the v1.0 charter was put through an **independent adversarial
review** — a six‑angle red team (a cheater, a metrologist, a chief scrutineer, a
privateer, a cross‑hardware architect, a governance/legal reviewer), each attacking the
rules; their proposed fixes were then **re‑attacked** by skeptics to confirm the patches
actually hold. The verdict was blunt and welcome:

> **v1.0 was not launch‑ready — it was gameable on day one — but the soul is sound and
> every hole is closable in a single v1.1 without bureaucratising the series.**

Publishing this review *is* the product: LLM Formula sells **honest, reproducible
numbers**, so it must survive being attacked in the open. This bulletin records the holes
and the controlling amendments. The binding measurement text now lives in
**[MEASUREMENT.md](MEASUREMENT.md)**; class/engine/interconnect changes are folded into
**[REGULATIONS.md](REGULATIONS.md) v1.1‑draft**.

## The critical holes found (all now addressed)

**Correctness gate (Art 6) — was statistically toothless**
- *99% top‑1 agreement* passes a stack whose every final answer is wrong: flip only the
  last answer token of a 300‑token chain → 0.33% disagreement → passes, math all wrong.
- "distributionally equivalent" speculative decoding was asserted, never tested.
- "≤1% degradation" had near‑zero statistical power and named no fixed suite.
- → **Fix:** teacher‑forced scoring; **critical‑span** gates (final answer / label / JSON
  value / refuse‑comply) at 100%; tie handling on softmax‑probability gap; **long‑context,
  refusal, and format sub‑gates**; powered **non‑inferiority** test on a sealed suite;
  tested distributional equivalence (mean TV ≤ 0.01) for sampled/spec stacks; scrutineering
  config **byte‑identical** to the timed run, run back‑to‑back (defeat‑device ban).

**Energy‑of‑Record (Art 2/4/7) — was not a hardware‑neutral invariant**
- AC "wall joules" folds in mains voltage + PSU efficiency (~16–54% swing on identical
  compute); the 1 s averaging let the whole run be one sub‑sample **1800 W burst with
  idle padding**; "software‑board + self‑declared overhead" let entrants delete 30–70% of
  joules; ±5% reproduction sat **below** the physical noise floor.
- → **Fix (MEASUREMENT.md):** canonical EoR = **AC‑mains, whole System‑Under‑Test, external
  meter**, over a defined **Active Window** (includes prefill + rejected draft tokens, no
  warm‑up before / idle inside); **true power**, hard peak ceiling + logged ≥1 kHz trace;
  **workload‑shaping/idle‑padding voids the run**; metering **tiers** (external scores,
  firmware = exhibition); a **no‑meter privateer path** with a published conservative
  constant + uncertainty band (no rank penalty); **steward median‑of‑3 is the figure of
  record**; reproduction judged on **combined expanded uncertainty**, not flat 5%.

**Accessibility & fairness**
- The only scoring engine (DeepSeek‑V4‑Flash q2 ~80 GB) needed ≥5 GPUs → "champion in a
  bedroom" was false; homologating a **GGUF file** made TensorRT/vLLM/MLX illegal by
  definition; the **NVLink ban** taxed only NVIDIA discrete multi‑GPU while on‑package
  fabrics ran free.
- → **Fix:** homologate the **model by reference‑output+logits fingerprint**, any
  quantization/runtime legal if it passes Art 6; **mandatory privateer‑tier engine**
  (≤24 GB VRAM + ≤128 GB unified‑memory/CPU) scoring full points every round; **interconnect
  ban withdrawn — Apple Silicon/AMD/CPU first‑class**; a **normalized "Engineering" sub‑score**
  (achieved ÷ roofline tok/J) so craft beats memory‑bus procurement.

**Governance, legal & safety — were asserted, not built**
- A GPU vendor could sponsor + co‑author the homologation + field a works team; the founder
  verified his own entry; CC‑BY cannot protect the **name** (a rogue series could fake
  "verified" numbers and stay CC‑compliant); 1 kW advice carried no electrical‑safety
  disclaimer and named Tonoken3 personally.
- → **Fix:** **Conflicted‑Partner recusal** (partners advise in public writing, never decide);
  a **named ≥3‑steward panel** with mandatory recusal and ≥2 signatures (the Series Director
  may **not** verify his own result); **protests & appeals** path; **IP‑protective** closed‑stack
  reproduction; documents stay CC‑BY but the **name/marks become a separate trademark +
  sanctioning license**; a **safety/liability disclaimer** behind a limited‑liability entity;
  engine **weights‑license** attestation.

## Honesty note
The skeptic pass found that several first‑round fixes were themselves **partial** — e.g.
a 1.3× / P99 power ceiling created fresh burst headroom; teacher‑forcing can mask error
accumulation; publishing reference logits can become a lookup table; a held‑out scored on
the steward's hardware collides with self‑submitting cloud/bedroom privateers. v1.1 adopts
the **refined** wording (tighter ceilings, sealed hold‑out with committed seed, live
steward reproduction with novel prompts, parity for meterless entrants). This is an
ongoing process: **v1.1 is hardened, not final**, and remains open to public comment.

## ⚑ Open decisions reserved to the founder
1. **Canonical EoR = AC‑wall** (adopted as default for accessibility) vs DC‑rail.
2. **GP1000 cap**: keep the iconic "1000" (= 1 kW *and* the 1000‑TPS horizon) vs a
   breaker‑safe continuous restatement (~900 W / dedicated circuit).
3. **Held‑out scoring**: confirm the live‑supervised‑reproduction path for privateers who
   can't ship a rig to a steward.
4. **Legal entity** (LLC/foundation) to hold the trademark + carry liability.
5. **Initial named steward panel**, and founder accepting recusal from his own DwarfStar4 entry.
6. **Cross‑vendor harness parity** (CPU/Metal/ROCm) milestone before GP400/E50 score points;
   until then those classes run as honestly‑labelled exhibition.

## Proposed calendar (integrity‑first)
**Bulletin 1 (this) → ~6–8 week public comment → Round 1 GP1000 shakedown (provisional points,
full reproduction loop exercised) → GP400/E50 open once cross‑vendor harness parity ships.**
Launch the rules first; earn the grid.

*Red‑team methodology and full per‑article amendment text archived by Lna‑Lab.*
