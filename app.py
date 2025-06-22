from flask import Flask, request, render_template, redirect, url_for, session
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)
app.secret_key = '1234'  # Needed for sessions

# Stepper motor GPIO pins
motor1_pins = [18, 17, 27, 22]
motor2_pins = [23, 24, 25, 5]

# Step sequence
step_seq = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Speed settings
SPEEDS = {
    'fast': 0.0015,
    'medium': 0.003,
    'slow': 0.006
}

GPIO.setmode(GPIO.BCM)

def setup(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def move_motor(pins, steps, delay):
    for _ in range(steps):
        for step in step_seq:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

def run_both_motors(speed_label):
    delay = SPEEDS.get(speed_label, SPEEDS['medium'])
    t1 = threading.Thread(target=move_motor, args=(motor1_pins, 512, delay))
    t2 = threading.Thread(target=move_motor, args=(motor2_pins, 512, delay))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    devices = ["baseboard-1", "petbrush-2", "vacuum-3"]
    return render_template("dashboard.html", devices=devices)

@app.route("/activate", methods=["POST"])
def activate():
    device = request.form.get("device")
    speed = request.form.get("speed", "medium")
    print(f"Toggling device: {device} at {speed} speed")

    if "baseboard" in device.lower() or "motor" in device.lower():
        run_both_motors(speed)

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    try:
        setup(motor1_pins)
        setup(motor2_pins)
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()
