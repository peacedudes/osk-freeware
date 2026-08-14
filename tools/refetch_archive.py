#!/usr/bin/env python3
"""Re-fetch the five OSK archive categories missing from the pool.

notes/DOWNLOADS-68k.md records 419 files fetched from Microware's OS-9 Archive;
the pool kept 281. DRIVERS, EFFO, GWINDOWS, NETWORK and TELECOM are absent
entirely -- 153 archives that nothing in AUDIT-pool.md has examined.

The archive runs Phoca Download behind a POST form: each file page carries a
per-session CSRF token, and the download is a POST of
{Itemid, license_agree, download=<id>, <token>=1} back to the same URL. So each
file needs its page fetched first. One request at a time with a pause between,
because this is someone else's server.
"""
import http.cookiejar, os, re, sys, time, urllib.parse, urllib.request

BASE = "https://microware.com"
CATS = {"DRIVERS": 105, "EFFO": 108, "GWINDOWS": 122, "NETWORK": 127, "TELECOM": 134}
UA = "Mozilla/5.0 (osk-freeware preservation; contact via github.com/peacedudes)"
PAUSE = 1.5

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [("User-Agent", UA)]


def get(url):
    with opener.open(url, timeout=120) as r:
        return r.read()


def listing(cat_id, name):
    """Every (file_id, filename) in a category, following its pagination."""
    out, start = [], 0
    while True:
        url = "%s/index.php/os-9-archive-new/category/%d-%s?start=%d" % (BASE, cat_id, name.lower(), start)
        html = get(url).decode("utf-8", "replace")
        ids = re.findall(r'/os-9-archive-new/file/(\d+)-', html)
        names = re.findall(r'>\s*([A-Za-z0-9._+-]+\.(?:lzh|zoo|ar|tar|gz|Z|zip|lha|uue|txt|bin|readme|doc|info|shar|tgz|ytar|lsm|hlp|1st|03|lhz|a|c|h))\s*<', html)
        fresh = [i for i in dict.fromkeys(ids) if i not in {x[0] for x in out}]
        if not fresh:
            break
        for k, i in enumerate(fresh):
            out.append((i, names[k] if k < len(names) else "file%s" % i))
        start += 20
        time.sleep(PAUSE)
    return out


def download(file_id, dest):
    """Fetch the file page for a token, then POST the licence form."""
    page_url = "%s/index.php/os-9-archive-new/file/%s-os-9-archive" % (BASE, file_id)
    html = get(page_url).decode("utf-8", "replace")
    m = re.search(r'name="phocaDownloadForm".*?</form>', html, re.S)
    if not m:
        return "no form"
    form = m.group(0)
    fields = dict(re.findall(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"', form))
    fields["submit"] = "Download"
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(page_url, data=data, headers={"User-Agent": UA, "Referer": page_url})
    with opener.open(req, timeout=300) as r:
        ctype = r.headers.get("Content-Type", "")
        body = r.read()
    if "text/html" in ctype:
        return "got HTML not a file"
    open(dest, "wb").write(body)
    return "ok %d bytes" % len(body)


def main():
    os.makedirs("refetch", exist_ok=True)
    log = open("refetch/refetch.log", "a")
    for name, cid in CATS.items():
        files = listing(cid, name)
        print("%-9s %3d files" % (name, len(files)), flush=True)
        d = os.path.join("refetch", name)
        os.makedirs(d, exist_ok=True)
        for fid, fname in files:
            dest = os.path.join(d, fname)
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                continue
            try:
                r = download(fid, dest)
            except Exception as e:
                r = "FAIL %s" % type(e).__name__
            line = "%-9s %-32s id=%-5s %s" % (name, fname, fid, r)
            print("  " + line, flush=True)
            log.write(line + "\n"); log.flush()
            time.sleep(PAUSE)


main()
