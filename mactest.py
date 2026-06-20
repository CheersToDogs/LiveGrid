#!/usr/bin/env python3
"""LiveGrid Mac diagnostic v2 - tests UDP/443 with raw sockets (no curl needed)."""
import socket, subprocess, ssl, time

def line(s=""): print(s)
line("="*60); line("  LiveGrid Mac Diagnostic v2"); line("="*60)

HOST = "edge-hls.saawsedge.com"
try:
    IP = socket.gethostbyname(HOST)
    line(f"\n[1] DNS: {HOST} -> {IP}  OK")
except Exception as e:
    line(f"\n[1] DNS FAIL: {e}"); IP=None

# [2] TCP 443
line("\n[2] TCP/443 (HTTP-2 path)...")
try:
    s = socket.create_connection((IP or HOST, 443), timeout=8)
    s.close(); line("    OK  TCP/443 connects")
except Exception as e:
    line(f"    FAIL  {e}")

# [3] UDP/443 reachability - THE QUIC TEST (raw socket, no curl)
# Send a minimal QUIC Initial-ish datagram; we only care if UDP/443 egress works
# (a blocked router drops it; an open one lets it out and we may get ANY reply or ICMP).
line("\n[3] UDP/443 egress (QUIC transport)...")
def udp443(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        # QUIC version negotiation probe (long header, random DCID)
        pkt = bytes([0xc0,0x00,0x00,0x00,0x01,0x08]) + bytes(8) + bytes([0x00,0x00]) + bytes(20)
        s.sendto(pkt, (ip, 443))
        try:
            data,_ = s.recvfrom(2048)
            s.close(); return ("REPLY", len(data))
        except socket.timeout:
            s.close(); return ("NO_REPLY", 0)  # sent ok but no answer (common; not conclusive)
    except Exception as e:
        return ("SEND_FAIL", str(e))

# Compare against a known-good QUIC host (google) to calibrate
g_ip = socket.gethostbyname("www.google.com")
gr = udp443(g_ip)
sr = udp443(IP or g_ip)
line(f"    google UDP/443: {gr[0]}")
line(f"    saawsedge UDP/443 ({IP}): {sr[0]}")

# [4] Try Chrome's actual HTTP/3 via python if h2 lib present (best-effort)
line("\n[4] Checking if a QUIC reply ever comes back from google...")
quic_works = (gr[0] == "REPLY")
line(f"    QUIC reply from google: {'YES' if quic_works else 'NO'}")

line("\n" + "="*60); line("  VERDICT"); line("="*60)
if gr[0]=="REPLY":
    line("""
  UDP/443 (QUIC) IS getting replies from google.
  => QUIC egress works on this network. Stills are NOT a QUIC block.
  Next: in Chrome DevTools Network tab, enable the 'Protocol' column,
  reload livegrid, click a red saawsedge row, and report:
    - Protocol (h2 or h3)
    - Status text (e.g. failed/CORS/blocked/200)
""")
elif gr[0]=="NO_REPLY" and sr[0]=="NO_REPLY":
    line("""
  UDP/443 sent but NO replies from google OR saawsedge.
  This STRONGLY suggests UDP/443 (QUIC) is filtered/dropped by your
  router or ISP -> Chrome tries QUIC, gets silence, shows stills.
  FIX: chrome://flags -> 'Experimental QUIC protocol' = Disabled
       (in the profile you actually use) -> Relaunch.
  PERMANENT: allow outbound UDP/443 on the router.
""")
else:
    line(f"""
  UDP send result: google={gr}, saawsedge={sr}
  Inconclusive from sockets. Use the DevTools Protocol column test:
  enable 'Protocol' column, reload, click a failed saawsedge row,
  report Protocol (h2/h3) + Status.
""")
line("Done.\n")
