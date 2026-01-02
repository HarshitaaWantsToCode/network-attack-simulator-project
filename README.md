# network-attack-simulator-project
Website to simulate DOS and replay and defend against them
Cyber Defense Dashboard — Locally Deployed Website
A lightweight Flask web app that demonstrates common security scenarios—DoS detection & prevention, MITM, and Replay attacks—in a safe, educational environment. Includes an optional Scapy-based script to simulate a UDP flood locally for testing rate‑limit behavior.

✨ Features

Home dashboard linking to individual simulations:

DoS Detection: flags rapid requests from the same IP within a time window (does not block).
DoS Prevention: rate‑limits and blocks when the request threshold is exceeded (HTTP 429). 
MITM Simulation: intercepts submitted form data and shows it back (for demo). 
Replay Attack Simulation: captures and replays the same payload multiple times (for demo). 


Local UDP Flood Simulator (simulate_dos.py) using Scapy—target defaults to 127.0.0.1 and port 53. ⚠️ For local lab use only. 


🧩 Architecture Overview

Flask app (app.py) serving four routes:

/ (Home)
/dos_detect (detection only)
/dos_prevent (detection + blocking)
/mitm_simulation (GET/POST)
/replay_simulation (GET/POST)
Each route renders minimal in‑code HTML templates via render_template_string. Rate limiting uses REQUEST_LIMIT and TIME_WINDOW with an in‑memory request_log. 


UDP flood script (simulate_dos.py) crafting and sending packets via Scapy: IP(dst=...) / UDP(dport=...). Includes pacing via time.sleep(delay). 


🛠️ Tech Stack

Python 3.10+ (recommended)
Flask for the web server and routes 
Scapy (optional) for local UDP flood simulations 


✅ Prerequisites

Python 3.x installed
(Optional) Npcap / packet driver if using Scapy on Windows (admin rights may be required)
