import json, re, inspect
from collections import namedtuple
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

if not hasattr(inspect, "getargspec"):
    ArgSpec = namedtuple("ArgSpec", "args varargs varkw defaults")
    def getargspec(func):
        sig = inspect.signature(func)
        args, defaults, varargs, varkw = [], [], None, None
        for name, p in sig.parameters.items():
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
                args.append(name)
                if p.default is not p.empty:
                    defaults.append(p.default)
            elif p.kind == p.VAR_POSITIONAL:
                varargs = name
            elif p.kind == p.VAR_KEYWORD:
                varkw = name
        return ArgSpec(args, varargs, varkw, tuple(defaults) or None)
    inspect.getargspec = getargspec

ROOT    = Path(__file__).resolve().parent.parent
IN_DIR  = ROOT /  "data" / "albums_tokens"
OUT_DIR = ROOT / "data" / "albums_tokens_filtered"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STOP_RU = {
    "я","ты","он","оно","мы","вы","они",
    "меня","тебя","его","нас","вас","них",
    "мне","тебе","ему","нам","вам","им",
    "мой","твой","наш","ваш","их",
    "в","на","к","с","из","у","о","об","от","до","за","по","при","для","без","через","между",
    "и","а","но","или","если","что","чтобы","как","когда","потому","так","либо","хотя","даже",
    "же","ли","бы","вот","ведь","пусть","просто","только","еще","уже","лишь","да","нет",
    "здесь","там","сюда","туда","тогда","сейчас",
    "ах","ох","ай","ой","эх","уа","ура","эй",
    "два","три","четыре","пять","шесть","семь","восемь","девять","десять","дцать",
    "второй","третий",
    "не","это","эти","со","себя", "е","всё","все","есть","она", "её", "то","ещё","кто","был","моей","всегда", "ща","чем","эту","моё","про","твои","чё","ха",
    "мной", "мои", "твоя","моём", "ней", "где", "этот", "это", "весь", "моих", "теперь", "тобой","быть","воу","тут", "будет", "себе", "во",
    "свой", "свои", "эта", "были", "типа", "твою", "сам", "нами", "было", "щас", "этих", "мою","мною", "своей", "ни", "этом",
    "пау", "ими", "всем", "своим", "р", "всю", "ну", "моя", "вся", "уоу", "кроме", "м", "ей", "кх", "холо", "оу", "под"



}

STOP_EN = {
    "i","you","he","she","it","we","they","me","him","her","us","them",
    "my","your","his","our","their",
    "in","on","at","by","for","to","from","with","about","of",
    "and","but","or","if","when","because","so","that","while",
    "the","a","an","this","these","those",
    "just","even","only","also","still","already","too",
    "oh","ah","hey","wow","hmm","s","em","b","go", "p", "m", "yo", "ba", "k", "aye"
}

def filter_tokens(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in STOP_RU and t not in STOP_EN]

def process(path: Path, acc: List[Dict]) -> None:
    data = json.loads(path.read_text("utf-8"))
    for r in data:
        r["tokens"] = filter_tokens(r.get("tokens", []))
    out = OUT_DIR / f"{path.stem}_filtered.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    acc.extend(data)

def main() -> None:
    combined: List[Dict] = []
    for f in tqdm(IN_DIR.glob("*_tokens.json"), desc="filtering", ncols=80):
        process(f, combined)
    (OUT_DIR / "albums_tokens_filtered.json").write_text(
        json.dumps(combined, ensure_ascii=False, indent=2), "utf-8"
    )

if __name__ == "__main__":
    main()
