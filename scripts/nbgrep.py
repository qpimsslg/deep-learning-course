import json
import re
from pathlib import Path
import sys

def iter_sources(nb_path: Path):
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    for i, cell in enumerate(data.get("cells", [])):
        src = "".join(cell.get("source", []))
        yield i, cell.get("cell_type", "unknown"), src

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/nbgrep.py <pattern> [root=.]")
        raise SystemExit(2)

    pattern = re.compile(sys.argv[1], re.IGNORECASE)
    root = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(".")

    nbs = list(root.rglob("*.ipynb"))
    hits = 0

    for nb in nbs:
        for idx, ctype, src in iter_sources(nb):
            if pattern.search(src):
                hits += 1
                print(f"{nb}:{idx} ({ctype})")
                # по желанию: печатать контекст
                # print(src[:300], "\n---")

    print(f"\nTotal matches: {hits}")

if __name__ == "__main__":
    main()
