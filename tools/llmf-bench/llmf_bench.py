#!/usr/bin/env python3
"""llmf-bench — the LLM Formula reference measurement harness.

Runs an OpenAI-compatible inference endpoint over a sealed prompt set, measures
energy over the Active Window, scores the greedy correctness gate, and emits a
signed `llmf-result/2` manifest (see MEASUREMENT.md / REGULATIONS Art. 6-7).

Stdlib only — runs anywhere a privateer can (NVIDIA / AMD / Apple / CPU / cloud).

Energy-of-Record = AC-mains, whole System Under Test, external meter (canonical).
Tiers (MEASUREMENT.md §5):
  external-csv  -> sensor_class=external  (Tier A/B, SCORES)
  nvidia-smi    -> sensor_class=firmware  (exhibition only, 0 points)
  manual        -> sensor_class=manual    (declared avg, exhibition)

Usage:
  python3 llmf_bench.py run \
      --endpoint http://localhost:8080/v1 --model deepseek-v4-flash \
      --reference round1_practice.jsonl --class GP1000 --round 1 \
      --handle lna-lab --meter external-csv --meter-csv watts.csv \
      --idle-watts 51.6 --out result.json

reference jsonl: one object per line: {"id": "...", "prompt": "...",
                 "reference": "<full greedy reference output>",
                 "answer_span": "<optional critical span, exact/number match>"}
watts.csv:       header `unix_ts,watts` (whole-system AC watts), >=1 Hz.
"""
import argparse, json, hashlib, time, sys, threading, subprocess, re, urllib.request

SCHEMA = "llmf-result/2"


# ---------- endpoint ----------
def call_endpoint(base, model, prompt, max_tokens, temperature, api_key, chat):
    url = base.rstrip("/") + ("/chat/completions" if chat else "/completions")
    if chat:
        body = {"model": model, "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens, "temperature": temperature, "stream": False}
    else:
        body = {"model": model, "prompt": prompt, "max_tokens": max_tokens,
                "temperature": temperature, "stream": False}
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    if api_key:
        req.add_header("Authorization", "Bearer " + api_key)
    with urllib.request.urlopen(req, timeout=600) as r:
        resp = json.load(r)
    ch = resp["choices"][0]
    text = ch.get("message", {}).get("content") if chat else ch.get("text")
    usage = resp.get("usage", {})
    ctok = usage.get("completion_tokens")
    return (text or ""), ctok


# ---------- power meters ----------
class FirmwareSampler(threading.Thread):
    """nvidia-smi background sampler -> [(ts, total_watts)]. EXHIBITION tier."""
    def __init__(self, interval=0.2):
        super().__init__(daemon=True)
        self.interval, self.samples, self._stop = interval, [], threading.Event()

    def run(self):
        while not self._stop.is_set():
            try:
                out = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=power.draw",
                     "--format=csv,noheader,nounits"], text=True, timeout=5)
                w = sum(float(x) for x in out.split() if x.strip()
                        and x.replace(".", "", 1).isdigit())
                self.samples.append((time.time(), w))
            except Exception:
                pass
            self._stop.wait(self.interval)

    def stop(self):
        self._stop.set()


def integrate(samples, t0, t1):
    """Trapezoidal integral (joules) and mean watts over [t0,t1]."""
    pts = [(t, w) for t, w in samples if t0 <= t <= t1]
    if len(pts) < 2:
        return None, None, len(pts)
    j = 0.0
    for (ta, wa), (tb, wb) in zip(pts, pts[1:]):
        j += (wb + wa) / 2.0 * (tb - ta)
    span = pts[-1][0] - pts[0][0]
    return j, (j / span if span > 0 else None), len(pts)


def load_csv_watts(path):
    rows = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.lower().startswith("unix_ts"):
            continue
        a, b = ln.split(",")[:2]
        rows.append((float(a), float(b)))
    return rows


# ---------- correctness gate ----------
def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def num_or_none(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s or "")
    return m.group(0).rstrip("0").rstrip(".") if m else None


def score_gate(outputs, refs):
    exact = span = span_total = n = 0
    for o, r in zip(outputs, refs):
        n += 1
        if norm(o) == norm(r.get("reference", "")):
            exact += 1
        sp = r.get("answer_span")
        if sp is not None:
            span_total += 1
            ok = (norm(sp) in norm(o)) or (
                num_or_none(sp) is not None and num_or_none(sp) == num_or_none(o))
            span += 1 if ok else 0
    return {
        "n_prompts": n,
        "exact_match_rate": round(exact / n, 4) if n else 0.0,
        "critical_span_rate": round(span / span_total, 4) if span_total else None,
        "critical_spans_scored": span_total,
        "note": "client-side greedy gate (exact + critical-span). Teacher-forced "
                "top-1/logit + distributional gates are steward-side (need logprobs).",
    }


def run(a):
    refs = [json.loads(l) for l in open(a.reference, encoding="utf-8") if l.strip()]
    print(f"[llmf-bench] {len(refs)} prompts | endpoint {a.endpoint} | class {a.klass}",
          file=sys.stderr)

    sampler = None
    if a.meter == "nvidia-smi":
        sampler = FirmwareSampler()
        sampler.start()
        time.sleep(1.0)

    outputs, tok_total, tok_counted = [], 0, True
    t0 = time.time()
    for i, r in enumerate(refs):
        txt, ctok = call_endpoint(a.endpoint, a.model, r["prompt"], a.max_tokens,
                                  a.temperature, a.api_key, a.chat)
        outputs.append(txt)
        if ctok is None:
            tok_counted = False
        else:
            tok_total += ctok
        print(f"  [{i+1}/{len(refs)}] {ctok} tok", file=sys.stderr)
    t1 = time.time()
    window = t1 - t0
    if sampler:
        sampler.stop()

    # ---- energy ----
    if a.meter == "external-csv":
        rows = load_csv_watts(a.meter_csv)
        joules, mean_w, nsamp = integrate(rows, t0, t1)
        sensor_class, meter_tier = "external", ("A" if nsamp / max(window, 1) >= 1000 else "B")
    elif a.meter == "nvidia-smi":
        joules, mean_w, nsamp = integrate(sampler.samples, t0, t1)
        sensor_class, meter_tier = "firmware", "exhibition"
    else:  # manual
        mean_w = a.avg_watts
        joules = (a.avg_watts * window) if a.avg_watts else None
        nsamp, sensor_class, meter_tier = 0, "manual", "exhibition"

    if not tok_counted:
        # fallback: rough token estimate (whitespace*1.3) when usage absent
        tok_total = int(sum(len(o.split()) for o in outputs) * 1.3)

    tps = tok_total / window if window > 0 else None
    tpj = (tok_total / joules) if joules else None
    tpj_marg = None
    if joules and a.idle_watts is not None:
        dyn = joules - a.idle_watts * window
        tpj_marg = (tok_total / dyn) if dyn > 0 else None

    out_hash = hashlib.sha256("\x1e".join(outputs).encode()).hexdigest()
    gate = score_gate(outputs, refs)

    manifest = {
        "schema": SCHEMA,
        "season": 2026, "round": a.round, "discipline": a.discipline,
        "class": a.klass,
        "entrant": {"handle": a.handle, "privateer": a.privateer},
        "engine": {"name": a.model, "weights_sha256": "pending"},
        "chassis": {"name": a.chassis, "endpoint": a.endpoint},
        "workload": {"n_prompts": len(refs), "max_tokens": a.max_tokens,
                     "temperature": a.temperature, "reference_set": a.reference},
        "measurement": {
            "energy_domain": "ac-wall" if a.meter == "external-csv" else "firmware-board",
            "sensor_class": sensor_class, "meter_tier": meter_tier,
            "power_samples": nsamp, "tokens": tok_total, "tokens_counted": tok_counted,
            "wall_seconds": round(window, 3),
            "joules": round(joules, 1) if joules else None,
            "avg_system_watts": round(mean_w, 2) if mean_w else None,
            "idle_baseline_w": a.idle_watts,
        },
        "results": {
            "tokens_per_second": round(tps, 3) if tps else None,
            "tokens_per_joule": round(tpj, 5) if tpj else None,
            "tokens_per_joule_marginal": round(tpj_marg, 5) if tpj_marg else None,
        },
        "correctness": gate,
        "output_sha256": out_hash,
        "scoring_eligible": sensor_class == "external",
        "reproduction": {"steward_verified": False},
        "disclaimer": "Self-reported. Energy scores only with an EXTERNAL whole-system "
                      "meter (MEASUREMENT.md). firmware/manual = exhibition (0 points). "
                      "Steward median-of-3 on the hold-out is the figure of record.",
    }
    json.dump(manifest, open(a.out, "w"), indent=2, ensure_ascii=False)
    print(json.dumps(manifest["results"], indent=2), file=sys.stderr)
    print(f"[llmf-bench] wrote {a.out}  (tier={meter_tier}, scoring={manifest['scoring_eligible']})",
          file=sys.stderr)


def main():
    p = argparse.ArgumentParser(prog="llmf-bench")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="benchmark an OpenAI-compatible endpoint")
    r.add_argument("--endpoint", required=True, help="OpenAI-compatible base URL, e.g. http://host:8080/v1")
    r.add_argument("--model", required=True)
    r.add_argument("--reference", required=True, help="sealed prompt set jsonl")
    r.add_argument("--class", dest="klass", required=True, choices=["GP1000", "GP400", "E50"])
    r.add_argument("--round", type=int, default=0)
    r.add_argument("--discipline", default="efficiency", choices=["pace", "efficiency", "endurance"])
    r.add_argument("--handle", default="anonymous")
    r.add_argument("--privateer", action="store_true", default=True)
    r.add_argument("--chassis", default="unknown")
    r.add_argument("--meter", default="manual", choices=["external-csv", "nvidia-smi", "manual"])
    r.add_argument("--meter-csv", help="unix_ts,watts CSV for --meter external-csv")
    r.add_argument("--idle-watts", type=float, help="powered, model-loaded, zero-decode baseline")
    r.add_argument("--avg-watts", type=float, help="declared avg watts for --meter manual")
    r.add_argument("--max-tokens", type=int, default=256)
    r.add_argument("--temperature", type=float, default=0.0)
    r.add_argument("--api-key", default=None)
    r.add_argument("--chat", action="store_true", help="use /chat/completions")
    r.add_argument("--out", default="result.json")
    a = p.parse_args()
    if a.cmd == "run":
        if a.meter == "external-csv" and not a.meter_csv:
            p.error("--meter external-csv requires --meter-csv")
        run(a)


if __name__ == "__main__":
    main()
