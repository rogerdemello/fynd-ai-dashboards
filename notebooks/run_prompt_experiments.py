#!/usr/bin/env python3
"""Run small prompt experiments for Task 1 using a synthetic sample.

Behavior:
- Creates a small synthetic dataset (default 200 samples) to avoid large downloads.
- Implements 3 prompt strategies: baseline, few-shot, chain-of-thought.
- If `GEMINI_API_KEY` is set in the environment, it will call Google Gemini API.
  Otherwise it runs a fast simulation (no external calls) to keep storage and bandwidth low.

Outputs:
- `tasks/task1/results_{strategy}.csv` small CSVs with predictions.
"""
from __future__ import annotations
import os
import csv
import json
import random
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import google.generativeai as genai
except Exception:
    genai = None


OUTDIR = Path(__file__).resolve().parent / "task1_results"
OUTDIR.mkdir(parents=True, exist_ok=True)


def make_synthetic_sample(n: int = 200) -> List[Dict]:
    """Create a synthetic list of reviews with ground-truth stars.
    Designed to be small and diverse without external data.
    """
    pos_phrases = [
        "absolutely loved it", "highly recommend", "five stars", "will come again",
        "perfect experience", "delicious", "superb service"
    ]
    neg_phrases = [
        "terrible experience", "do not recommend", "one star", "never coming back",
        "awful", "horrible service", "very disappointing"
    ]
    neutral_phrases = [
        "it was okay", "average", "nothing special", "decent for the price",
        "not bad", "could be better"
    ]

    samples = []
    for i in range(n):
        star = random.choices([1,2,3,4,5], weights=[10,10,20,30,30], k=1)[0]
        if star >= 4:
            text = f"{random.choice(pos_phrases)} — the meal was great and staff were friendly."
        elif star == 3:
            text = f"{random.choice(neutral_phrases)} — the food was okay but service slow."
        else:
            text = f"{random.choice(neg_phrases)} — I had a bad time and won't recommend."
        samples.append({"id": i + 1, "review": text, "stars": star})
    return samples


def baseline_prompt(review: str) -> str:
    return (
        f"Classify the following Yelp review into 1-5 stars. Return only valid JSON with keys 'predicted_stars' (int)"
        f" and 'explanation' (short). Review: \"{review}\"\n\nRespond with JSON only."
    )


def few_shot_prompt(review: str) -> str:
    examples = [
        {"review": "Absolutely loved it, will come again.", "stars": 5},
        {"review": "It was okay, nothing special.", "stars": 3},
        {"review": "Terrible experience, very disappointing.", "stars": 1},
    ]
    ex_text = ""
    for ex in examples:
        ex_text += f"Review: \"{ex['review']}\" => {ex['stars']} stars\n"
    return (
        f"You are given examples:\n{ex_text}\nNow classify the following review into 1-5 stars and return JSON with 'predicted_stars' and 'explanation'."
        f" Review: \"{review}\"\nRespond with JSON only."
    )


def cot_prompt(review: str) -> str:
    return (
        "Read the review and think step-by-step about the sentiment, then output a JSON object."
        f" Review: \"{review}\"\nFirst give a short reasoning, then output the JSON with keys 'predicted_stars' and 'explanation'."
    )


def call_llm(prompt: str, model: str = "gemini-1.5-flash", timeout: int = 15) -> Tuple[bool, str]:
    """Call Google Gemini API if available. Returns (ok, text).
    If genai package or API key missing, returns (False, '')
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or genai is None:
        return False, ""
    genai.configure(api_key=api_key)
    try:
        model_obj = genai.GenerativeModel(model)
        resp = model_obj.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=256,
                temperature=0.2,
            )
        )
        text = resp.text.strip()
        return True, text
    except Exception as e:
        return False, str(e)


def parse_json_from_text(text: str) -> Tuple[bool, Dict]:
    """Attempt to extract JSON object from text.
    Returns (valid, obj_or_error).
    """
    try:
        # try direct parse
        obj = json.loads(text)
        return True, obj
    except Exception:
        # try to find first {...}
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                obj = json.loads(text[start : end + 1])
                return True, obj
            except Exception as e:
                return False, {"error": str(e), "raw": text}
        return False, {"error": "no json found", "raw": text}


def run_strategy(name: str, prompt_fn, samples: List[Dict], use_llm: bool) -> Dict:
    results = []
    for s in samples:
        prompt = prompt_fn(s["review"])
        if use_llm:
            ok, out = call_llm(prompt)
            if ok:
                valid, obj = parse_json_from_text(out)
                if valid and isinstance(obj, dict) and "predicted_stars" in obj:
                    pred = int(obj["predicted_stars"])
                    explanation = obj.get("explanation", "")
                    json_valid = True
                else:
                    pred = None
                    explanation = out
                    json_valid = False
            else:
                pred = None
                explanation = out
                json_valid = False
        else:
            # simulation: small noisy mapping from ground truth
            gt = s["stars"]
            pred = max(1, min(5, gt + random.choice([-1, 0, 1])))
            explanation = "(simulated) short justification"
            json_valid = True

        results.append(
            {
                "id": s["id"],
                "review": s["review"],
                "gold": s["stars"],
                "predicted": pred,
                "json_valid": json_valid,
                "explanation": explanation,
            }
        )

    # write CSV
    out_file = OUTDIR / f"results_{name}.csv"
    with out_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "review", "gold", "predicted", "json_valid", "explanation"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    # compute simple metrics
    valid_preds = [r for r in results if r["predicted"] is not None]
    accuracy = sum(1 for r in valid_preds if r["predicted"] == r["gold"]) / max(1, len(results))
    json_rate = sum(1 for r in results if r["json_valid"]) / max(1, len(results))

    return {"strategy": name, "accuracy": accuracy, "json_rate": json_rate, "n": len(results), "outfile": str(out_file)}


def main(n: int = 200):
    samples = make_synthetic_sample(n)
    use_llm = bool(os.environ.get("GEMINI_API_KEY")) and genai is not None
    if use_llm:
        print("GEMINI_API_KEY found — running real LLM calls (be aware of usage costs).")
    else:
        print("No GEMINI_API_KEY — running simulation to preserve storage and avoid external calls.")

    strategies = [
        ("baseline", baseline_prompt),
        ("few_shot", few_shot_prompt),
        ("chain_of_thought", cot_prompt),
    ]

    summaries = []
    for name, fn in strategies:
        print("Running strategy:", name)
        summ = run_strategy(name, fn, samples, use_llm)
        summaries.append(summ)
        print(summ)

    # write brief summary file
    summary_fp = OUTDIR / "summary.json"
    summary_fp.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print("Wrote results to", OUTDIR)


if __name__ == "__main__":
    main(200)
