#!/usr/bin/env python3
"""Harvest EFFO "Info" files from the recovered archives.

EFFO defined a standard metadata form and shipped one per program: a set of
$KEYWORD paragraphs, of which $PROGRAM-NAME, $PURPOSE, $SUMMARY,
$SOURCE-LANGUAGE, $SOURCE-AVAILABILITY and $AUTHOR-NAME are mandatory. That
availability line is the closest thing to a licence statement most of this
corpus has, and it comes from the author rather than from inference.

Info_empty_form is the blank template EFFO ships on every disk -- it is not a
program's metadata and is skipped, having otherwise made every disk look like
it carried shareware.
"""
import os, re, json

STAGE = "newstage"
KEY = re.compile(r"^\$([A-Z][A-Z0-9-]*)")

def parse(path):
    try:
        text = open(path, "rb").read().decode("latin-1")
    except OSError:
        return {}
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out, cur = {}, None
    for line in text.split("\n"):
        m = KEY.match(line)
        if m:
            cur = m.group(1)
            out.setdefault(cur, [])
        elif cur and line.strip():
            out[cur].append(line.strip())
    return {k: " ".join(v).strip() for k, v in out.items() if v}

records = []
for d, _, fs in os.walk(STAGE):
    for f in fs:
        if not re.match(r"(?i)info[._]", f):
            continue
        if "empty" in f.lower():
            continue
        rec = parse(os.path.join(d, f))
        name = rec.get("PROGRAM-NAME", "").split()[0] if rec.get("PROGRAM-NAME") else ""
        if not name:
            continue
        records.append({
            "name": name,
            "file": os.path.relpath(os.path.join(d, f), STAGE),
            "purpose": rec.get("PURPOSE", ""),
            "summary": rec.get("SUMMARY", "")[:300],
            "status": rec.get("STATUS", ""),
            "hardware": rec.get("HARDWARE", ""),
            "language": rec.get("SOURCE-LANGUAGE", ""),
            "availability": rec.get("SOURCE-AVAILABILITY", ""),
            "author": rec.get("AUTHOR-NAME", ""),
            "runtime": rec.get("RUNTIME-FILES", ""),
            "version": rec.get("VERSION", ""),
        })

records.sort(key=lambda r: r["name"].lower())
json.dump(records, open("effo_info.json", "w"), indent=1)
print("info files parsed:", len(records))
import collections
c = collections.Counter(r["availability"].lower()[:40] or "(blank)" for r in records)
print("\n$SOURCE-AVAILABILITY as stated by the authors:")
for k, v in c.most_common():
    print("  %3d  %s" % (v, k))
