#!/usr/bin/env python3
"""
LiveGrid Mac network diagnostic.
Tells you exactly why video won't play. Run:  python3 mactest.py
No installs needed (uses macOS built-in python3 + curl).
"""
import subprocess, json, socket, ssl, urllib.request, time

def sh(cmd, t=12):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=t)
        return (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"

def line(s=""): print(s)

line("="*60)
line("  LiveGrid Mac Network Diagnostic")
line("="*60)

# 1. DNS
line("\n[1] DNS resolution of saawsedge...")
try:
    ips = socket.gethostbyname_ex("edge-hls.saawsedge.com")[2]
    line(f"    OK  resolves -> {', '.join(ips)}")
except Exception as e:
    line(f"    FAIL  {e}")

# 2. TCP 443 (HTTP/2) reachability via curl
line("\n[2] TCP / HTTP-2 fetch (what curl/Mac uses)...")
out = sh("curl -sI --http2 'https://media-hls.saawsedge.com/b-hls-16/200459374/200459374_240p.m3u8' -H 'referer: https://livegrid.pages.dev/' --max-time 10 | head -1")
if out == "__TIMEOUT__": line("    FAIL  timed out (TCP/443 blocked)")
elif "200" in out or "30" in out: line(f"    OK  {out}")
else: line(f"    ?? {out or 'no response'}")

# 3. UDP 443 (QUIC) reachability  -- THE KEY TEST
line("\n[3] UDP / QUIC (HTTP-3) on port 443  <-- the usual culprit...")
out3 = sh("curl -sI --http3-only 'https://www.google.com/' --max-time 8 | head -1")
if out3 == "__TIMEOUT__" or out3 == "":
    line("    FAIL  UDP/443 (QUIC) is BLOCKED on this network.")
    line("          >>> THIS is why Chrome shows stills. <<<")
    quic_blocked = True
else:
    line(f"    OK  QUIC works: {out3}")
    quic_blocked = False

# 4. Does curl negotiate h3 to the CDN at all?
line("\n[4] Can QUIC reach the stream CDN specifically...")
out4 = sh("curl -sI --http3-only 'https://media-hls.saawsedge.com/b-hls-16/200459374/200459374_240p.m3u8' -H 'referer: https://livegrid.pages.dev/' --max-time 8 | head -1")
if out4 == "__TIMEOUT__" or out4 == "":
    line("    FAIL  QUIC to saawsedge times out (UDP/443 dropped)")
else:
    line(f"    OK  {out4}")

# Verdict
line("\n" + "="*60)
line("  VERDICT")
line("="*60)
if quic_blocked:
    line("""
  Your network BLOCKS UDP port 443 (QUIC / HTTP-3).
  - curl works because it uses TCP.
  - Chrome tries QUIC first -> silently fails -> stills.

  TWO FIXES:
  A) Quick (per Chrome profile, can reset):
     chrome://flags -> search 'quic'
     -> 'Experimental QUIC protocol' = Disabled -> Relaunch
     Do this in the SAME profile you actually browse in.

  B) Permanent (router): allow OUTBOUND UDP port 443.
     Then QUIC works and you never touch the flag again.
""")
else:
    line("""
  QUIC is NOT blocked here. The stills are something else.
  Send Ken's assistant the output above + in Chrome DevTools
  Network tab, the 'Protocol' (h2/h3) and 'Status' of a failed
  saawsedge row.
""")
line("Done.\n")
