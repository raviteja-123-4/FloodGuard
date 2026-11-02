import math
from collections import Counter
import pandas as pd
from scapy.all import PcapReader, IP, TCP, UDP, ICMP

WINDOW = 0.5  # seconds

FILES = [
    ("data/normal.pcap",      "normal", 0),
    ("data/attack_syn.pcap",  "syn",    1),
    ("data/attack_udp.pcap",  "udp",    1),
    ("data/attack_http.pcap", "http",   1),
]

def entropy(counter):
    total = sum(counter.values())
    if not total:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counter.values())

def new_bucket():
    return {"pkts": 0, "bytes": 0, "syn": 0, "ack": 0, "udp": 0,
            "icmp": 0, "src": Counter()}

def to_row(b, label, kind):
    return {
        "pps": b["pkts"] / WINDOW,
        "syn_ack_ratio": b["syn"] / max(b["ack"], 1),
        "unique_src": len(b["src"]),
        "src_entropy": entropy(b["src"]),
        "avg_size": b["bytes"] / max(b["pkts"], 1),
        "udp_ratio": b["udp"] / max(b["pkts"], 1),
        "icmp_ratio": b["icmp"] / max(b["pkts"], 1),
        "label": label,
        "attack_type": kind,
    }

def process(path, kind, label):
    rows, bucket, start = [], new_bucket(), None
    for pkt in PcapReader(path):
        if IP not in pkt:
            continue
        t = float(pkt.time)
        if start is None:
            start = t
        while t - start >= WINDOW:
            if bucket["pkts"] > 0:
                rows.append(to_row(bucket, label, kind))
            bucket, start = new_bucket(), start + WINDOW
        bucket["pkts"] += 1
        bucket["bytes"] += len(pkt)
        bucket["src"][pkt[IP].src] += 1
        if TCP in pkt:
            f = int(pkt[TCP].flags)
            if f & 0x02 and not f & 0x10:
                bucket["syn"] += 1
            if f & 0x10:
                bucket["ack"] += 1
        elif UDP in pkt:
            bucket["udp"] += 1
        elif ICMP in pkt:
            bucket["icmp"] += 1
    if bucket["pkts"] > 0:
        rows.append(to_row(bucket, label, kind))
    return rows

all_rows = []
for path, kind, label in FILES:
    r = process(path, kind, label)
    print(f"{path}: {len(r)} windows")
    all_rows += r

df = pd.DataFrame(all_rows)
df.to_csv("data/dataset.csv", index=False)
print(df.groupby("attack_type").mean(numeric_only=True).round(2))
