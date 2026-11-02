# FloodGuard: ML-Based DDoS Detection & Mitigation System

FloodGuard is an intrusion detection and automated mitigation system designed to detect and respond to Distributed Denial of Service (DDoS) attacks in network traffic using machine learning.

## Features & Architecture

FloodGuard implements a complete end-to-end detection pipeline:

1. **Traffic Generation & Capture**:
   - 	raffic_normal.py: Simulates legitimate client requests.
   - ttack_http.py: Simulates high-rate HTTP/SYN/UDP flood attacks.
2. **Feature Extraction (eatures.py)**:
   - Analyzes raw packet captures (.pcap) across sliding time windows (.5\text{s}$).
   - Computes statistical features:
     - pps: Packets per second
     - syn_ack_ratio: Ratio of SYN packets to ACK packets
     - unique_src: Number of distinct source IP addresses
     - src_entropy: Shannon entropy of source IP distribution
     - vg_size: Average packet size (bytes)
     - udp_ratio: Ratio of UDP packets to total packets
     - icmp_ratio: Ratio of ICMP packets to total packets
   - Outputs aggregated features to data/dataset.csv.
3. **Machine Learning Model (detect.py)**:
   - Trains a RandomForestClassifier on extracted traffic features.
   - Evaluates performance metrics (Precision, Recall, F1-score) and exports model.pkl.
4. **Alerting System (lerts.py)**:
   - Real-time logging of detected attack events with confidence scores.
5. **Automated Mitigation (espond.py)**:
   - Automated simulated blacklisting / firewall blocking of malicious source IPs.
6. **Main Pipeline Runner (main.py)**:
   - Orchestrates model loading, evaluation on incoming traffic windows, alert triggering, and response actions.

## Quick Start

### 1. Requirements & Setup
`ash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
`

### 2. Feature Extraction
Extract features from pcap captures into dataset:
`ash
python3 features.py
`

### 3. Model Training
Train the Random Forest classifier:
`ash
python3 detect.py
`

### 4. Run Detection & Mitigation
Test the live inference pipeline:
`ash
python3 main.py
`

