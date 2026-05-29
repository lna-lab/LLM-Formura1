# Homologated Engines — the Constructors' Grid

**Season 1 (2026) · proposed roster · companion to [REGULATIONS.md](REGULATIONS.md) Art. 5**

In LLM Formula the **engine is the model**. The world's open‑weight champions are the
spec engines; the **labs supply the engines, the world's privateers are the drivers.**
The contest is not *whose model is smartest* — the labs already fight that on quality
benchmarks — it is **who runs a given engine with the fewest joules per token.** Same
engine, every garage on Earth, one ranking: tokens‑per‑joule.

A round names its engine(s); a season **tours** them like circuits — one round on a
Chinese flagship, the next on an American or French one — so the championship spans the
whole open‑weight world.

## The proposed grid (Season 1)

> Flags = the engine's lab of origin. Versions are **forward‑looking targets**; each is
> confirmed at its round's homologation bulletin (see "How an engine is homologated").

### 🏁 GP1000 — Grand Prix (≤ 1 000 W) · the flagship MoEs
| Engine | Lab · Origin |
|---|---|
| **DeepSeek‑V4** | DeepSeek · 🇨🇳 |
| **Nemotron‑3 Ultra** | NVIDIA · 🇺🇸 |
| **MiniMax‑3.0** | MiniMax · 🇨🇳 |
| **Kimi‑K2.6** | Moonshot AI · 🇨🇳 |
| **GLM‑5.1** | Zhipu / Z.ai · 🇨🇳 |

### ⚙️ GP400 — the grid (≤ 400 W) · single‑GPU / Mac / capped multi‑GPU
| Engine | Lab · Origin |
|---|---|
| **Gemma‑4** | Google · 🇺🇸 |
| **Qwen3.6** | Alibaba · 🇨🇳 |
| **Mistral Small** (candidate) | Mistral · 🇫🇷 |

### 🔋 E50 — Edge (≤ 50 W) · laptops / Apple Silicon / Jetson
| Engine | Lab · Origin |
|---|---|
| **Bonsai** (ultra‑compact) | origin TBC |
| **LFM2.5‑8B‑A1B** | Liquid AI · 🇺🇸 |
| **Ministral 3B** (candidate) | Mistral · 🇫🇷 |

> 🌍 **The flags tell the story.** China (DeepSeek, MiniMax, Kimi, GLM, Qwen), the USA
> (Nemotron, Gemma, Liquid), France (Mistral). Rival nations' engines on one grid, raced
> by privateers everywhere. *That* is the show.

## How an engine is homologated (Art. 5.1)

An engine joins the roster only when its round's bulletin pins all of:
1. **License & AUP cleared** — the upstream model license must permit homologation,
   derivative quantization, redistribution (or direct‑from‑source download), and
   **publication of benchmark numbers**. Permissive (Apache‑2.0 / MIT) is simplest;
   custom community licenses (e.g. some flagship terms) are admitted only if these uses
   are allowed. Entrants attest license compliance in the manifest.
2. **Format‑neutral master + quant spec** — a bit‑defined reference (e.g. safetensors
   BF16) plus a written quantization spec. Any realization (GGUF q‑x, TensorRT INT4‑AWQ,
   MLX 4‑bit, …) is legal if it passes the gate.
3. **Reference output + logits fingerprint** — a frozen per‑round artifact (pinned
   fp32‑logit, deterministic reduction) that the correctness gate (Art. 6) scores against,
   runnable offline on any accelerator — so a non‑NVIDIA stack never has to execute a
   vendor‑specific engine to be judged.
4. **Privateer‑tier guarantee** — every round homologates at least one GP400 engine
   runnable in ≤ 24 GB VRAM **and** a unified‑memory/CPU variant in ≤ 128 GB RAM, both
   scoring full points, so a Mac or a single consumer GPU genuinely contests the grid.

## Status

This roster is a **proposal for community comment** (Bulletin 1 window). Exact versions,
availability, and licenses are confirmed per round before points are awarded. Suggest an
engine or flag a license issue via a repository Issue titled `[Homologation] <engine>`.

🏁 *The world's engines. The world's tuners. One ranking — tokens per joule.*
