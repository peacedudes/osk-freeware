#!/bin/bash
# netpbm.sh -- run the NETPBM cluster and check it still works.
#
#   tools/recipes/netpbm.sh [image]        default: ./osk-freeware.dd
#
# This is a RECIPE, not a unit test: every command below is one a person can
# type at the shell on this disk, and DOC/HOWTO prints the same ones. If this
# script passes, the instructions we ship are true.
#
# NOT part of tools/check_disk.py, deliberately. check_disk is fast and needs
# no emulator; this needs os9exec and takes minutes.
#
# FOUR THINGS THAT WILL BITE YOU, all found by getting them wrong first:
#
#  1. os9exec converts CR to CRLF on its way out to the host, so a raw raster
#     containing byte 0x0D comes back with an 0x0A injected after it. Measured
#     on a 256-level ramp: 275 bytes where 274 was right. NEVER compare raw
#     image bytes captured on the host. OS-9's own pipes are clean -- all 256
#     values survive -- so keep binary inside OS-9 and bring back only text.
#
#  2. Some converters SEEK in their input and cannot read a pipe. pcxtoppm
#     and sgitopnm both fail with "error seeking past header" when piped, and
#     both work perfectly given a filename. They are marked `file' below.
#
#  3. pbmtext dies with "**** Stack Overflow ****" at the default storage
#     size. -mm 256k is enough for everything here.
#
#  4. Several formats have a FIXED canvas -- MacPaint is always 576x720, an
#     Atari ST PI3 always 640x400. A round trip through them SHOULD change the
#     dimensions, so they are checked against the size the format mandates,
#     not against the source.
#
# The check is the image TYPE AND DIMENSIONS returned by pnmfile, not the
# raster. Several of these formats legitimately change type -- GIF always
# comes back as PPM -- so comparing pixels would fail working programs.
set -u

IMG=${1:-osk-freeware.dd}
[ -f "$IMG" ] || { echo "no such image: $IMG (build it with tools/mkimage.sh)"; exit 2; }
IMG=$(cd "$(dirname "$IMG")" && pwd)/$(basename "$IMG")

command -v os9exec >/dev/null || { echo "os9exec not on PATH"; exit 2; }
TMO=""; command -v gtimeout >/dev/null && TMO="gtimeout 60"

PASS=0; FAIL=0
P='PATH=/dd/CMDS:/dd/CMDS/GAMES:/dd/CMDS/NETPBM:.; export PATH'

# Run one command line on the disk and return its output with CRs stripped.
run() {
  $TMO env OS9DISK="$IMG" os9exec -mm 256k -r bash -c "$P; $1" </dev/null 2>&1 \
    | tr -d '\r' | grep -viE '^$|shell cwd was reset|^# /h0:'
}

# check <label> <expected-substring> <command>
check() {
  local label=$1 want=$2 cmd=$3 got
  got=$(run "$cmd")
  if printf '%s' "$got" | grep -qF "$want"; then
    PASS=$((PASS+1)); printf '  ok    %s\n' "$label"
  else
    FAIL=$((FAIL+1)); printf '  FAIL  %s\n        want: %s\n        got : %s\n' \
      "$label" "$want" "$(printf '%s' "$got" | head -2 | tr '\n' ' ')"
  fi
}

echo "NETPBM recipe -- $IMG"
echo
echo "Generators (need no input file at all):"
check "pbmmake makes a PBM"      "PBM"          "pbmmake -g 16 8 | pnmfile"
check "pgmramp makes a PGM"      "32 by 16"     "pgmramp -lr 32 16 | pnmfile"
check "ppmmake makes a PPM"      "32 by 16"     "ppmmake rgb:80/40/c0 32 16 | pnmfile"
check "pbmtext renders text"     "PBM"          "pbmtext os9 | pnmfile"

echo
echo "The shipped demo image:"
check "sphere.pgm is readable"   "48 by 24"     "pnmfile /dd/DEMO/sphere.pgm"
check "sphere renders as ASCII"  "MMMM"         "pnminvert /dd/DEMO/sphere.pgm | pgmtopbm -threshold -value 0.5 | pbmtoascii"
check "pnmscale halves it"       "24 by 12"     "pnmscale 0.5 /dd/DEMO/sphere.pgm | pnmfile"
check "pnmflip turns it"         "24 by 48"     "pnmflip -cw /dd/DEMO/sphere.pgm | pnmfile"

echo
echo "Round trips -- export to a foreign format and read it back:"
PBM="pbmtext os9"          ; PBMSIZE="46 by 29"
PGM="pgmramp -lr 32 16"    ; PGMSIZE="32 by 16"
PPM="ppmmake rgb:80/40/c0 32 16"

# pipeable pairs that come back the same size
for row in "atk pbmtoatk atktopbm" "cmuwm pbmtocmuwm cmuwmtopbm" \
           "gem pbmtogem gemtopbm" "mgr pbmtomgr mgrtopbm" \
           "xbm pbmtoxbm xbmtopbm" "ybm pbmtoybm ybmtopbm" \
           "g3 pbmtog3 g3topbm"; do
  set -- $row
  check "$1" "$PBMSIZE" "$PBM | $2 | $3 | pnmfile"
done
for row in "bmp ppmtobmp bmptoppm" "gif ppmtogif giftopnm" \
           "ilbm ppmtoilbm ilbmtoppm" "pict ppmtopict picttoppm" \
           "pj ppmtopj pjtoppm" "tga ppmtotga tgatoppm" \
           "xpm ppmtoxpm xpmtoppm"; do
  set -- $row
  check "$1" "32 by 16" "$PPM | $2 | $3 | pnmfile"
done
for row in "fits pnmtofits fitstopnm" "rast pnmtorast rasttopnm" \
           "sir pnmtosir sirtopnm" "xwd pnmtoxwd xwdtopnm" \
           "fs pgmtofs fstopgm"; do
  set -- $row
  check "$1" "$PGMSIZE" "$PGM | $2 | $3 | pnmfile"
done

echo
echo "Round trips onto a FIXED canvas -- the size change is the format:"
check "icon pads to a byte"  "48 by 29"   "$PBM | pbmtoicon | icontopbm | pnmfile"
check "macp MacPaint page"   "576 by 720" "$PBM | pbmtomacp > /dd/tmp/r.macp; macptopbm /dd/tmp/r.macp | pnmfile"
check "pi3 Atari ST hi-res"  "640 by 400" "$PBM | pbmtopi3 > /dd/tmp/r.pi3; pi3topbm /dd/tmp/r.pi3 | pnmfile"
check "pi1 Atari ST lo-res"  "320 by 200" "$PPM | ppmtopi1 > /dd/tmp/r.pi1; pi1toppm /dd/tmp/r.pi1 | pnmfile"

echo
echo "Round trips that need a real file, because the reader seeks:"
check "pcx" "32 by 16" "$PPM | ppmtopcx > /dd/tmp/r.pcx; pcxtoppm /dd/tmp/r.pcx | pnmfile"
check "sgi" "32 by 16" "$PGM | pnmtosgi > /dd/tmp/r.sgi; sgitopnm /dd/tmp/r.sgi | pnmfile"

echo
echo "Round trips with a constraint of their own:"
check "yuv needs the dimensions given"  "32 by 16" "$PPM | ppmtoyuv | yuvtoppm 32 16 | pnmfile"
check "lispm needs maxval 16 or less"   "32 by 16" "$PGM | pnmdepth 15 | pgmtolispm | lispmtopgm | pnmfile"

echo
printf '%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
