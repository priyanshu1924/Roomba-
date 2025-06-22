# Raspberry Pi Web-Controlled Stepper Motor with Login

This project sets up a **Flask web server on a Raspberry Pi 2W running Raspberry Pi OS Lite (32-bit)**. The server hosts a login page and provides secure web-based control of stepper motors connected to the Pi's GPIO pins.

---

## 🧰 Features

- Responsive, animated **login page**
- Login authentication using hardcoded credentials
- Stepper motor control via Flask routes
- GPIO control using `RPi.GPIO`
- Deployed and accessed remotely over SSH
- Hosted entirely on a **headless Raspberry Pi (no desktop environment)**

---

## 🧾 Requirements

- Raspberry Pi 2W (or similar)
- Raspberry Pi OS Lite (32-bit)
- SSH enabled
- Stepper motor and driver (e.g., 28BYJ-48 + ULN2003)
- Wires and 5V power source

---

## 📡 Raspberry Pi Setup (Once)

1. Flash **Raspberry Pi OS Lite (32-bit)** to an SD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
2. Enable SSH by placing an empty file called `ssh` in the `boot` partition.
3. Connect to Wi-Fi by editing `wpa_supplicant.conf` in the `boot` partition.
4. Boot the Pi and connect via SSH:

   ```bash
   ssh pi@<your_pi_ip>
   ```

   If the `pi` user is disabled, use your custom username like:

   ```bash
   ssh amal@<your_pi_ip>
   ```

---

## 📦 Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install flask RPi.GPIO
```

---

## 📁 Project Structure

```
esp32web/
├── motor_server.py        # Flask backend
└── templates/
    └── login.html         # Styled login page
```

---

## 🔐 Login System

- HTML login page with animations is located in `templates/login.html`.
- Credentials are hardcoded in `motor_server.py`:

```python
USER_CREDENTIALS = {
    "username": "admin",
    "password": "password123"
}
```

> ✅ You can change this later to use a secure database or environment variables.

---

## 🔌 Stepper Motor Control

- Uses GPIO pins **17, 18, 27, 22** for motor control.
- Connect motor driver (e.g., ULN2003) to those pins.
- Motor rotates when visiting `/motor1` route.

---

## ▶️ Running the App

On your Pi:

```bash
python3 motor_server.py
```

It will run the Flask server at:

```
http://<your_pi_ip>:5000
```

---

## 💻 Uploading Files Over SSH

From your Windows PC:

```powershell
scp "C:\path\to\login.html" amal@<your_pi_ip>:/home/amal/templates/login.html
```

---

## 🧪 Test the Web App

1. Visit `http://<your_pi_ip>:5000/`
2. Log in with `admin / password123`
3. You'll be redirected to `/motor-control`
4. Click the motor link to activate the stepper

---

## ✅ Notes

- Developed and deployed on **Raspberry Pi OS Lite (32-bit)**.
- Managed entirely over SSH (`scp`, `ssh`, `nano`).
- Do **not** expose this to the public internet without HTTPS and proper authentication.

---

## 🧠 Future Ideas

- Add logout and session protection
- Replace hardcoded credentials with hashed auth
- Add control UI with motor direction/speed
- Build a REST API for more advanced control