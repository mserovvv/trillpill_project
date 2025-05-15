import inspect
import json
import re
from collections import namedtuple
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

if not hasattr(inspect, 'getargspec'):
    ArgSpec = namedtuple('ArgSpec', 'args varargs varkw defaults')
    def getargspec(func):
        sig = inspect.signature(func)
        args = []
        defaults = []
        varargs = None
        varkw = None
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

ROOT = Path(__file__).resolve().parent.parent
IN_DIR = ROOT / 'data' / 'albums'
OUT_DIR = ROOT / 'data' / 'albums_tokens'
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOK_RE = re.compile(r'[а-яё\*a-z]+', re.I)
BRACKETS = re.compile(r'\[[^\]]*]|\([^)]*\)')

def tokenize(text: str) -> List[str]:
    clean = BRACKETS.sub(' ', text)
    return TOK_RE.findall(clean)

def process(path: Path, acc: List[Dict]) -> None:
    data = json.loads(path.read_text('utf-8'))
    for record in data:
        record['tokens'] = tokenize(record['lyrics_raw'])
    out_file = OUT_DIR / f"{path.stem.replace('_clear', '')}_tokens.json"
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), 'utf-8')
    acc.extend(data)

def main() -> None:
    combined: List[Dict] = []
    for fname in tqdm(IN_DIR.glob('*_clear.json'), desc='albums', ncols=80):
        process(fname, combined)
    combined_file = OUT_DIR / 'albums_tokens.json'
    combined_file.write_text(json.dumps(combined, ensure_ascii=False, indent=2), 'utf-8')

if __name__ == '__main__':
    main()
