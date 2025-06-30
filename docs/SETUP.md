# 🌌 AXISABLE CELESTIAL — Setup Instructions

Welcome to **Celestial**, your fully local, offline-first AI education system.

---

## 🖥️ Quick Start (Recommended)

1. Plug in your USB or unzip this folder to your desktop.
2. Double-click:  
3. The Celestial interface will launch in the background with tray access.

---

## ⚙️ Developer Mode (Advanced)

If you want to rebuild the system from source:

1. Open `run_build_and_test.bat`
2. This will:
- Install packages from `offline_packages/`
- Run automated voice + memory tests
- Build `CELESTIAL.exe` using PyInstaller

No internet connection is required.

---

## 🗣 Wake Word (Coming Soon)

You’ll soon be able to say:
> “Hey Celeste”

To activate the voice engine.  
(For now, use the tray or click to activate.)

---

## 🔒 Child Mode

To enable safe content mode:
- Create the file: `child_mode.lock`
- Or toggle from the system tray when available

This filters content, suppresses NSFW lessons, and restricts certain agents.

---

## 📂 Folder Structure

```plaintext
AXISABLE_CELESTIAL_USB_BOOT/
├── agents/               # Delta, Lyra, Kairos, Noor
├── assets/               # Icons, avatars, GUI graphics
├── core/                 # Voice, memory, child_mode modules
├── interface/            # Celestial main GUI code
├── offline_packages/     # Full offline Python package wheelhouse
├── tests/                # Unit tests for core functions
├── CELESTIAL.exe         # Your launchable GUI
├── start_here.bat        # Recommended launcher
├── run_build_and_test.bat# Full rebuild + test script
└── .env, requirements.txt, CELESTIAL.spec
