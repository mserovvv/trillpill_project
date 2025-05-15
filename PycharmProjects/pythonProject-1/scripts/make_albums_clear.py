import json
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).resolve().parent.parent
IN_DIR = ROOT / "data" / "albums"
OUT_DIR = IN_DIR
OUT_DIR.mkdir(parents=True, exist_ok=True)


def clean(text: str) -> str:
    lines = [ln.strip() for ln in text.lower().splitlines() if ln.strip()]
    return "\n".join(lines)


def process(path: Path, acc: List[Dict]) -> None:
    recs = json.loads(path.read_text("utf-8"))
    for r in recs:
        r["lyrics_raw"] = clean(r["lyrics_raw"])
    clr = path.with_stem(path.stem + "_clear")
    clr.write_text(json.dumps(recs, ensure_ascii=False, indent=2), "utf-8")
    acc.extend(recs)


def main() -> None:
    out: List[Dict] = []
    for f in IN_DIR.glob("*.json"):
        if f.stem.endswith("_clear"):
            continue
        process(f, out)
    (OUT_DIR / "albums_clear.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), "utf-8"
    )


if __name__ == "__main__":
    main()
