# 🏁 LLM Formula

### The World Championship of Inference Efficiency
### 推論効率の世界選手権

> # 🔥 「お前のトークンで札束を燃やすな。情熱を燃やせ。」
> ### Don't burn cash with your tokens — burn passion.

*The privateer's creed: you don't win by buying the biggest cluster. You win by engineering the cleverest joule.*
*プライベーターの信条：最大のクラスタを買った者ではなく、最も賢い1ジュールを設計した者が勝つ。*

> **FLOPs are free. The only fight is bandwidth, latency, and joules.**
> **演算はタダだ。我々が戦うのは、帯域・遅延・そしてジュールである。**

*Issued by **Lna-Lab** · Season 1 (2026) · Charter date: 2026‑05‑29*

---

## What this is / これは何か

**LLM Formula** is an open, global motorsport-style championship for **large-language-model inference**. Competitors — from lone privateers with a pair of consumer GPUs to works teams with server racks — race the *same homologated model* and are scored on how well they convert **electricity into tokens**.

Modern Formula 1 is not a contest of raw horsepower; since the hybrid era it is an **energy-efficiency formula** — a fixed fuel allowance, and victory to whoever converts it most cleverly into speed. **LLM Formula applies the same spirit to AI inference.** The headline metric is **tokens-per-joule**. The craft is in the tune: quantization, batching, kernel fusion, clock/voltage control, parallel topology, speculative decoding.

You do not need the biggest cluster. You need the best engineering.

**LLM Formula** は、大規模言語モデル**推論**のための、オープンで世界規模のモータースポーツ型選手権です。民生GPU2枚のプライベーターから、サーバーラックを擁するワークスチームまで——**同一の公認モデル**を走らせ、**電力をいかに上手くトークンへ変換したか**で競います。

現代のF1は単なる馬力競争ではありません。ハイブリッド時代以降、それは**エネルギー効率のフォーミュラ**——決められた燃料を、誰が最も賢く速さに変えるか、です。**LLM Formula はその思想をAI推論に持ち込みます。** 主役の指標は **tokens‑per‑joule（1ジュールあたりのトークン数）**。腕の見せ所はチューニング：量子化・バッチ処理・カーネル融合・クロック/電圧制御・並列トポロジ・投機デコード。

最大のクラスタは要りません。要るのは、最高のエンジニアリングです。

---

## The Championships / 選手権

| 称号 Title | 指標 Metric | 性格 Character |
|---|---|---|
| 🏆 **Pace** (Fastest Lap) | 単騎ピーク tokens/s | 予選アタック — レイテンシの腕 |
| 🏆 **Efficiency** (the blue riband) | **tokens / joule** (wall energy) | ハイブリッド燃費 — エンジニアリングの真価 |
| 🏆 **Endurance** (Constructors') | 電力上限下の集約 tokens/s | ル・マン — スループットの総合力 |

## The Classes — a power formula / クラス（電力フォーミュラ）

Classes are defined by **sustained wall power** — our equivalent of the fuel-flow regulation. There is **no unlimited / works-only class**: by design every class, including the flagship, is runnable by **an individual, in any country, from a single domestic mains outlet.** The World Champion may live in a bedroom, not a datacenter.

| Class | 電力上限 Power cap | 接続 Interconnect | 想定 Who |
|---|---|---|---|
| **GP1000 — Grand Prix** | ≤ 1 000 W | **PCIe-only** | 家庭の壁コンセント1つで世界中どこでも引ける上限。マルチGPUプライベーターの最高峰 |
| **GT300** | ≤ 300 W | **PCIe-only** | 単プロシューマGPU / 電力制限マルチGPU。効率の中堅 |
| **E50 — Edge** | ≤ 50 W | single-node | ノート、Apple Silicon、Jetson、電力制限の単機。エコの極北 |

> **Why 1 kW?** A continuous ~1 kW draw fits one household circuit **everywhere** — even Japan's 100 V/15 A (~1.5 kW) clears it. So the *top* class is open to every individual on Earth, not just server rooms. NVLink and proprietary fabric are banned in GP1000/GT300 — you race on consumer PCIe. (なぜ1000Wか：どの国の個人でも家庭の商用電力で参戦できるように。)
>
> Reference rig **DwarfStar4** (7× RTX PRO 2000 Blackwell, PCIe, ~490 W board active) races in **GP1000**.

---

## How to enter / 参戦方法

1. Read the **[Regulations](REGULATIONS.md)** — the technical & sporting rulebook.
2. Run a **homologated engine** (spec model) on your hardware.
3. Pass **scrutineering**: your output must match the reference within tolerance — *you cannot win by breaking the model.* 正答性 > 速度.
4. Submit a **result manifest** (see **[ENTRY.md](ENTRY.md)**): hardware, model checksum, energy trace, token count, wall time, output hash.
5. A steward independently reproduces your run. Verified times go on the **leaderboard**.

Privateers welcome. Open source encouraged. Glory to the cleverest joule.

---

## Call for Partners & Sponsors / 協賛企業の募集

LLM Formula is a stage for **sustainable, efficient AI** and for the engineers who build it. We invite:

- **GPU / accelerator vendors**, **PSU / cooling / power** makers, **cloud & datacenter** providers — as **Technical Partners**.
- **Title & Series sponsors** who want their name on the championship of AI efficiency.
- A **Privateer Support Fund** — hardware grants so a brilliant tuner anywhere on Earth can enter.

See **[PARTNERS.md](PARTNERS.md)**. Reach the people optimizing the future of inference, measured — not marketed.

LLM Formula は、**持続可能で効率的なAI** と、それを支えるエンジニアたちの舞台です。GPU/アクセラレータ、電源・冷却、クラウド/データセンターの各社を**テクニカルパートナー**として、また**タイトル協賛**・**プライベーター支援基金**を広く募ります。詳細は **[PARTNERS.md](PARTNERS.md)**。

---

## Status / 現況

- **Season 1 (2026)** — charter & regulations published 2026‑05‑29. Inaugural rounds, homologation list, and the public leaderboard are opening now.
- Founder & Series Director: **Tonoken3 / Lna‑Lab**.
- Technical supervision & measurement methodology: **Claude Opus 4.8** (the reference scrutineering harness is built on the open **DwarfStar4** engine).

Regulations & docs are offered openly to the world (CC BY 4.0). Fork them, run a round, start a national series. The grid is open.

> 🏁 *Let the World Grand Prix begin.* ワールドグランプリを、始めよう。
