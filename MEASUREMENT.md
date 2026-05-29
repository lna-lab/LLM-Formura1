# LLM Formula — Measurement Standard (MEASUREMENT.md)

**v0.9 DRAFT · 2026‑05‑29 · companion to REGULATIONS Art. 2/4/6/7**

*This is the scrutineer's handbook: how a token‑per‑joule figure is defined, measured, and reproduced so that an NVIDIA multi‑GPU rig, an Apple‑Silicon laptop, an AMD APU, a CPU node, and a cloud instance produce **comparable** numbers. It was hardened by an adversarial review (Bulletin 1). Items marked ⚑ are **founder decisions** still open.*

## 1. The Energy‑of‑Record (EoR)

⚑ **Canonical EoR = AC‑mains energy of the entire System Under Test, measured by an *external* instrument, integrated over the Active Window, in joules.**

- We use **AC‑wall** as canonical (not DC‑rail) because it is the only figure that (a) encloses the *whole* system including PSU/VRM/host/cooling losses, (b) is measurable by laptops, Apple Silicon, single‑board edge, and cloud instances that have **no accessible DC rails**, and (c) is what a single domestic outlet physically sees — matching the series' founding principle. DC‑rail energy is **supplementary** (it excludes PSU conversion loss and would reward a titanium PSU bought at the same outlet).
- **External instrument** = a meter electrically independent of the measured device's firmware (inline AC meter / smart plug / clamp). `nvidia-smi`/NVML/RAPL/vendor SDK power is **firmware telemetry**, not external, and is exhibition‑only.

**Report two figures, always:** `tokens_per_joule_gross = tokens / E_window` and `tokens_per_joule_marginal = tokens / (E_window − idle_baseline_w × window_seconds)`. Marginal makes a fat‑host discrete rig and a lean SoC comparable on *compute* energy.

## 2. The Active Window

Bounded by the **first byte of prompt delivered to the engine** and the **last decoded token of the scored generation**. It **includes** all energy the run requires — prefill, weight load/graph capture/autotune/cache priming if performed inside the window, speculative draft generation, and **rejected** draft tokens. **No interval may be excluded or shifted outside** the window or the manifested `wall_seconds`; warm‑up may not be done *before* the window to make measured decode look free. Naturally‑occurring DVFS/idle *during legitimate decode* is fine — that is not "insertion."

## 3. System Under Test (SUT) boundary

**One metered envelope** enclosing every device doing *any* inference‑related work: target + draft models, scheduler, tokenizer, sampling, de‑tokenization, host pre/post‑processing. No cross‑node offload; no host carve‑out. (E50: single metered host. GP1000/GP400: all accelerators behind one meter.) Mandatory `idle_baseline_w` = system powered, model loaded, zero decode.

## 4. Power & the class cap (true power, real instruments)

- **True (real) power in watts**, never apparent power (VA); power factor ≥ 0.9 or report PF and use real power.
- **Two binding cap tests:** (i) Active‑Window **average** ≤ class cap; (ii) **hard ceiling** — P99.9 of 100 ms samples and the max of 1 s rolling averages both ≤ 1.00× cap; brief sub‑100 ms transients tolerated to 1.15× only if over‑cap excursion energy < 2 % of run energy.
- **Workload‑shaping ban:** you may not schedule energy‑intensive tokens into over‑cap windows and pad with low‑power active filler. The scored stream is contiguous.
- **No‑fault re‑run:** an externally‑caused supply interruption (e.g. a shared‑circuit trip) is a re‑run, not a black flag — stewards may cap re‑runs and require evidence.

## 5. Measurement tiers (all map to AC‑wall joules)

| Tier | Method | Status |
|---|---|---|
| **A** | ≥1 kHz external AC meter, full power time‑series + stats attached | **Scores**; required for records / runs within 5 % of cap |
| **B** | calibrated low‑rate (≥1 Hz) external meter / smart plug; or DC‑rail log **with declared PSU‑efficiency curve** converting to AC‑wall | **Scores** below cap, ranked under Tier A, steward‑verified |
| **C** | cloud whole‑node PMBus/Redfish/PDU, **single‑tenant only** | **Scores** if whole‑node |
| **D** | no‑meter: harness estimate from board telemetry + **published conservative** per‑platform PSU & host floor | Enters with a **bounded‑uncertainty band** (ranked at the least‑favourable bound), upgraded on one external cross‑check |
| — | software‑board only + self‑declared overhead | **Exhibition, 0 points** |

A points entry is valid only if `sensor_class = external`, `energy_sensor_scope = full-SUT`, and `sensor_accuracy_pct ≤ 2`.

## 6. Correctness coupling

A time only counts if the **same byte‑identical build/config/power‑policy** passed scrutineering **back‑to‑back** with the timed run (REGULATIONS Art. 6 / 11.6). The leaderboard figure is set on a **held‑out** sealed slice the entrant never tuned against. Teacher‑forced top‑1 + **critical‑span** + distributional (for sampled/spec) gates; see Art. 6.

## 7. Reproduction & uncertainty

- The **steward's** measurement (median of N ≥ 3 reps) is the **figure of record**, not the entrant's claim.
- Reproduction succeeds when steward and entrant agree within the **combined expanded uncertainty (k=2, 95 %)** of both — not a flat ±5 % (which sits below the silicon/thermal/mains noise floor).
- Thermal soak to steady state before the window; report `ambient_temp_c` (25 ± 2 °C reference), sustained clocks, driver/firmware. Leakage ≈ 2× power per ~10 °C — ambient is a confound, control it.
- Reproduction failure **downgrades to provisional**; only fraud or refusal voids.

## 8. Manifest fields (schema v2 additions)

`energy_domain {ac-wall|dc-rail}`, `sensor_class {external|firmware}`, `energy_sensor_scope`, `sensor_accuracy_pct`, `mains_voltage_v`, `psu_model`, `psu_80plus_tier`, `psu_load_fraction`, `idle_baseline_w`, `power_trace_url`, `power_factor`, `watts_mean/rms/p99/p999/peak`, `sample_rate_hz`, `meter_tier`, `tenancy`, `provider`, `instance_type`, `aggregate_mem_bandwidth_GBps`, `accelerators[] {vendor,model,count,mem_bytes,mem_bandwidth_GBps}`, `memory_model {discrete|unified|numa}`, `validated_context_len`, `tokens_per_joule_marginal`, `config_hash`, `expanded_uncertainty_pct`.

## 9. The one‑command harness

`llmf-bench` (in `tools/llmf-bench/`) runs an OpenAI‑compatible engine + scrutineering + metering and emits the signed manifest + power trace automatically. A privateer never hand‑edits JSON. See its README.

---

### ⚑ Open founder decisions (gate the standard)
1. **AC‑wall vs DC‑rail as canonical EoR** (we default to AC‑wall for accessibility + whole‑system honesty).
2. **GP1000 cap**: keep round "1000 W" nameplate, or restate to a breaker‑safe continuous figure (~900 W / "dedicated circuit").
3. **Held‑out scoring vs self‑submission**: stewards operating the entrant's rig is impossible for many privateers — confirm the live‑supervised‑reproduction path.
4. **Cross‑vendor harness parity** milestone before GP400/E50 score points (CPU/Metal/ROCm).

*Bulletin 1 records the full adversarial review and proposed Article amendments.*
