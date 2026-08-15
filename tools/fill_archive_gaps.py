#!/usr/bin/env python3
"""Fetch whatever the OS-9 archive lists that the pool does not hold.

Works by NAME, not by count: a category page is scraped for (file id, name)
pairs and anything whose name is absent from the pool is downloaded. Counting
alone was misleading -- GCC and GNU hold more locally than the site lists,
because those came from elsewhere.

Same Phoca POST/CSRF dance as tools/refetch_archive.py.
"""
import http.cookiejar, os, re, time, urllib.parse, urllib.request, sys

BASE = "https://microware.com"
A = "/Users/rdoggett/mine/os9/xxx/os9exec/os9/PUBCMDS/microware-archive"
UA = "Mozilla/5.0 (osk-freeware preservation; contact via github.com/peacedudes)"
CATS = {"apps":99,"archivers":102,"cmds":103,"demos":104,"drivers":105,"effo":108,
        "games":110,"gcc":112,"gnu":117,"graphics":121,"gwindows":122,"languages":124,
        "lib":125,"misc":126,"network":127,"shells":131,"src":132,"telecom":134}
PAUSE = 1.2

jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
op.addheaders = [("User-Agent", UA)]

def get(u):
    with op.open(u, timeout=120) as r:
        return r.read()

def listing(name, cid):
    """(id, filename) pairs, from the <a> title text next to each file link."""
    out, start, seen = [], 0, set()
    while True:
        h = get("%s/index.php/os-9-archive-new/category/%d-%s?start=%d" % (BASE, cid, name, start)).decode("utf-8","replace")
        pairs = re.findall(r'/os-9-archive-new/file/(\d+)-[^"]*"[^>]*>\s*([^<]+?)\s*<', h)
        fresh = [(i, n) for i, n in pairs if i not in seen]
        if not fresh:
            break
        for i, n in fresh:
            seen.add(i); out.append((i, n))
        start += 20; time.sleep(PAUSE)
    return out

def download(fid, dest):
    page = "%s/index.php/os-9-archive-new/file/%s-os-9-archive" % (BASE, fid)
    h = get(page).decode("utf-8", "replace")
    m = re.search(r'name="phocaDownloadForm".*?</form>', h, re.S)
    if not m:
        return "no form"
    fields = dict(re.findall(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"', m.group(0)))
    fields["submit"] = "Download"
    req = urllib.request.Request(page, data=urllib.parse.urlencode(fields).encode(),
                                 headers={"User-Agent": UA, "Referer": page})
    with op.open(req, timeout=300) as r:
        if "text/html" in r.headers.get("Content-Type", ""):
            return "got HTML"
        body = r.read()
    open(dest, "wb").write(body)
    return "ok %d bytes" % len(body)

total = 0
for name, cid in sorted(CATS.items()):
    d = os.path.join(A, name.upper())
    os.makedirs(d, exist_ok=True)
    have = {f.lower() for f in os.listdir(d)}
    files = listing(name, cid)
    missing = [(i, n) for i, n in files
               if n.lower() not in have and re.search(r"\.[A-Za-z0-9]{1,4}$", n)]
    if not missing:
        print("%-11s %3d listed, nothing missing" % (name, len(files))); continue
    print("%-11s %3d listed, %d missing" % (name, len(files), len(missing)))
    for fid, fn in missing:
        try:
            r = download(fid, os.path.join(d, fn))
        except Exception as e:
            r = "FAIL %s" % type(e).__name__
        print("    %-34s %s" % (fn, r)); total += 1
        time.sleep(PAUSE)
print("\nfetched:", total)
