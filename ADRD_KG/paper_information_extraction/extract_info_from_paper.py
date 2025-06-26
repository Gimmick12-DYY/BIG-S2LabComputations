#!/usr/bin/env python
"""
extract_info_from_text.py  ▸  Minimal script to pull dataset-level metadata
from a cleaned plain-text full paper using an LLM.

Usage
-----
$ python extract_info_from_text.py \
        --txt_file  /path/to/cleaned_PMC8640037.txt \
        --output_dir /path/to/dataset_info \
        --model      gpt-4.1            # optional
"""

import os, json, argparse, asyncio
from agents import Agent     # your existing wrapper

# -------------------------------------------------------------------
DATASET_PROMPT = """
You are an expert biomedical reader. Extract all the datasets and data types
used in the following full-text article.  Return **valid JSON** with keys:
- Dataset_Names
- Dataset_Sources
- Data_Types
- Brain_Regions
- Cohort_Info
- Preprocessing_Tools
- Analysis_Tools
- Key_Findings

Text:
<<FULLTEXT>>
"""
# -------------------------------------------------------------------
async def extract_dataset_info(txt_path: str, model: str = "gpt-4.1"):
    """Read cleaned text, send to LLM, return parsed JSON (dict)."""
    with open(txt_path, "r", encoding="utf-8") as fh:
        full_text = fh.read().strip()
    if not full_text:
        return None

    prompt = DATASET_PROMPT.replace("<<FULLTEXT>>", full_text[:45_000]) 
    # (45 k chars ≈ 11-12k tokens, adjust if your model’s context >/ < that.)

    agent = Agent(model=model)
    return await agent.process(prompt, step=0, response_format="JSON")


# -------------------------------------------------------------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--txt_file",   required=True, help="Clean full-text .txt file")
    p.add_argument("--output_dir", default="dataset_info", help="Where to save JSON")
    p.add_argument("--model",      default="gpt-4.1")
    args = p.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(
        args.output_dir,
        os.path.basename(args.txt_file).replace(".txt", ".json"),
    )

    try:
        result = asyncio.run(extract_dataset_info(args.txt_file, args.model))
        if result:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"[✅] Saved extraction → {out_path}")
        else:
            print("[❌] No content / extraction failed.")
    except Exception as e:
        print("[❌] LLM extraction error:", e)
