#SET 4
#Question - 17

import json #iam imprting json here
from pathlib import Path

try:
    import yaml #imprting in the try block fr btr 
except ImportError:
    yaml = None


def load_any(path: str):
    p = Path(path)
    text = p.read_text()

    if p.suffix.lower() in [".yaml", ".yml"]:
        if yaml is None:
            raise RuntimeError("pyyaml not there")
        return yaml.safe_load(text)
    return json.loads(text)


def split_by_key(records: list[dict], key: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for rec in records:
        value = str(rec.get(key, "UNKNOWN"))
        groups.setdefault(value, []).append(rec)
    return groups


def split_and_save(in_path: str, key: str, out_prefix: str = "out_"):
    data = load_any(in_path)
    

    

    if not isinstance(data, list):
        raise ValueError("Expected a list of rcrd at top lvl")
    grouped = split_by_key(data, key)
    for value, records in grouped.items():
        safe_value = value.replace(" ", "_").lower()
        out_name = f"{out_prefix}{safe_value}.json"
        Path(out_name).write_text(json.dumps(records, indent=2))
        print(f"Saved {len(records)} records to {out_name}")


if __name__ == "__main__":
    


    sample = [
        {"id": 1, "region": "APAC", "status": "open"},
        {"id": 2, "region": "EMEA", "status": "closed"},
        {"id": 3, "region": "APAC", "status": "in_progress"},
    ]
    Path("tasks.json").write_text(json.dumps(sample))

    split_and_save("tasks.json", key="region")
