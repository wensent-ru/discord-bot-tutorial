import json


def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(filename, content):
    with open(filename, "w") as outfile:
        json.dump(content, outfile, ensure_ascii=True, indent=4)
