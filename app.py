from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# --- Configuration for DoS Simulations ---
REQUEST_LIMIT = 20  # Max requests
TIME_WINDOW = 10    # In seconds
request_log = {}    # Dictionary to store request timestamps

# --- HTML Templates (Embedded for simplicity) ---

# 1. Home Page Template
HOME_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cyber Defense Dashboard</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #1c1c1c; color: #f0f0f0; text-align: center; padding-top: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; background-color: #2e2e2e; border: 1px solid #444; border-radius: 8px; }
        h1 { color: #00ffcc; }
        a.button { color: #1c1c1c; background-color: #00ffcc; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 4px; margin: 15px; display: inline-block; }
        a.button:hover { background-color: #00ccaa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cyber Defense Dashboard</h1>
        <p>Choose a simulation to run:</p>
        <a href="/dos_detect" class="button">1. DoS Detection</a>
        <a href="/dos_prevent" class="button">2. DoS Prevention</a>
        <a href="/mitm_simulation" class="button">3. MITM Simulation</a>
        <a href="/replay_simulation" class="button">4. Replay Attack Simulation</a>
    </div>
</body>
</html>
"""

# 2. General Simulation Page Template
SIMULATION_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #1c1c1c; color: #f0f0f0; text-align: center; padding-top: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; background-color: #2e2e2e; border: 1px solid #444; border-radius: 8px; }
        h1 { color: #00ffcc; }
        .result { font-size: 1.2em; padding: 20px; margin-top: 20px; border: 1px solid #666; background-color: #444; color: {{ color }}; }
        a.link { color: #00ffcc; margin-top: 20px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p>{{ description }}</p>
        <div class="result">{{ message }}</div>
        <a href="/" class="link">← Back to Home</a>
    </div>
</body>
</html>
"""

# 3. MITM Simulation Form Page
MITM_FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MITM Simulation</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #1c1c1c; color: #f0f0f0; text-align: center; padding-top: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; background-color: #2e2e2e; border: 1px solid #444; border-radius: 8px; }
        h1, h2 { color: #00ffcc; }
        .result { margin-top: 20px; padding: 10px; background-color: #444; border: 1px solid #666; border-radius: 4px; color: #fff; }
        a.link { color: #00ffcc; margin-top: 20px; display: inline-block; }
        input[type=text] { padding: 10px; width: 80%; background-color: #1c1c1c; border: 1px solid #666; color: #f0f0f0; border-radius: 4px; }
        button { background-color: #00ffcc; color: #1c1c1c; padding: 10px 20px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; margin: 20px; }
        button:hover { background-color: #00ccaa; }
    </style>
</head>
<body>
    <div class="container">
        <h2>MITM Simulation</h2>
        <p>Simulate a message being intercepted by an attacker.</p>
        <form method="POST">
            <label for="message">Your Message:</label><br><br>
            <input type="text" name="message" required><br>
            <button type="submit">Send Message</button>
        </form>
        {% if intercepted %}
            <div class="result">{{ intercepted }}</div>
        {% endif %}
        <a href="/" class="link">← Back to Home</a>
    </div>
</body>
</html>
"""

# 4. Replay Attack Simulation Form Page
REPLAY_FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Replay Attack Simulation</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #1c1c1c; color: #f0f0f0; text-align: center; padding-top: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; background-color: #2e2e2e; border: 1px solid #444; border-radius: 8px; }
        h1, h2 { color: #00ffcc; }
        .result { margin-top: 20px; padding: 10px; background-color: #444; border: 1px solid #666; border-radius: 4px; color: #fff; }
        a.link { color: #00ffcc; margin-top: 20px; display: inline-block; }
        input[type=text] { padding: 10px; width: 80%; background-color: #1c1c1c; border: 1px solid #666; color: #f0f0f0; border-radius: 4px; }
        button { background-color: #00ffcc; color: #1c1c1c; padding: 10px 20px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; margin: 20px; }
        button:hover { background-color: #00ccaa; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Replay Attack Simulation</h2>
        <p>Simulate a message being intercepted and replayed by an attacker.</p>
        <form method="POST">
            <label for="message">Your Message:</label><br><br>
            <input type="text" name="message" required><br>
            <button type="submit">Send Message</button>
        </form>
        {% if replayed_message %}
            <div class="result">
                <p>Original Message Captured: '{{ replayed_message }}'</p>
                <p>Attacker replays the message...</p>
                <p>Replayed Message Sent: '{{ replayed_message }}'</p>
                <p>Replayed Message Sent: '{{ replayed_message }}'</p>
            </div>
        {% endif %}
        <a href="/" class="link">← Back to Home</a>
    </div>
</body>
</html>
"""

# --- Application Routes ---

@app.route('/')
def home():
    """Renders the main navigation page."""
    return render_template_string(HOME_PAGE_HTML)

@app.route('/dos_detect')
def dos_detect():
    """Detects and flags a DoS attack but does NOT block the request."""
    ip = request.remote_addr
    now = time.time()
    if ip not in request_log: request_log[ip] = []
    request_log[ip].append(now)
    request_log[ip] = [t for t in request_log[ip] if now - t < TIME_WINDOW]

    if len(request_log[ip]) > REQUEST_LIMIT:
        msg, color = f"⚠️ DoS Attack Detected! Requests in last {TIME_WINDOW}s: {len(request_log[ip])}", "#ff4d4d"
    else:
        msg, color = f"✅ Normal Traffic. Requests in last {TIME_WINDOW}s: {len(request_log[ip])}", "#00ffcc"
    
    return render_template_string(SIMULATION_PAGE_HTML, title="Detection Only", description="This page flags an attack but won't block you. Refresh rapidly.", message=msg, color=color)

@app.route('/dos_prevent')
def dos_prevent():
    """Detects a DoS attack and BLOCKS the request."""
    ip = request.remote_addr
    now = time.time()
    if ip not in request_log: request_log[ip] = []
    request_log[ip].append(now)
    request_log[ip] = [t for t in request_log[ip] if now - t < TIME_WINDOW]

    if len(request_log[ip]) > REQUEST_LIMIT:
        msg = "Rate limit exceeded. Request Blocked."
        return render_template_string(SIMULATION_PAGE_HTML, title="Detection & Prevention", description="This page identifies and BLOCKS an attack. Refresh rapidly.", message=msg, color="#ff4d4d"), 429
    else:
        msg = f"✅ Normal Traffic. Requests in last {TIME_WINDOW}s: {len(request_log[ip])}"
        return render_template_string(SIMULATION_PAGE_HTML, title="Detection & Prevention", description="This page identifies and BLOCKS an attack. Refresh rapidly.", message=msg, color="#00ffcc")

@app.route('/mitm_simulation', methods=['GET', 'POST'])
def mitm():
    """Simulates a Man-in-the-Middle attack by intercepting form data."""
    intercepted_message = None
    if request.method == 'POST':
        message = request.form.get('message')
        intercepted_message = f"🔍 Intercepted Message: '{message}'"
    return render_template_string(MITM_FORM_HTML, intercepted=intercepted_message)

@app.route('/replay_simulation', methods=['GET', 'POST'])
def replay():
    """Simulates a Replay attack by capturing and replaying form data."""
    replayed_message = None
    if request.method == 'POST':
        message = request.form.get('message')
        # In a real replay attack, the attacker would capture and resend the *entire* request.
        # Here, we simulate by just showing the message multiple times.
        replayed_message = message
    return render_template_string(REPLAY_FORM_HTML, replayed_message=replayed_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')