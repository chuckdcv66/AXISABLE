import subprocess
import sys
import os
import json
from pathlib import Path

REQUIRED_PACKAGES = [
    "PyQt5",
    "PyQtWebEngine"
]

VSCODE_SETTINGS_PATH = Path(".vscode") / "settings.json"
EXTRA_PATHS = ["./core"]

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")

def patch_vscode_paths():
    try:
        os.makedirs(".vscode", exist_ok=True)
        settings = {}
        if VSCODE_SETTINGS_PATH.exists():
            with open(VSCODE_SETTINGS_PATH, "r", encoding="utf-8") as f:
                settings = json.load(f)

        existing = set(settings.get("python.analysis.extraPaths", []))
        for path in EXTRA_PATHS:
            existing.add(path)

        settings["python.analysis.extraPaths"] = sorted(existing)

        with open(VSCODE_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

        print(f"🧠 VS Code paths updated: {EXTRA_PATHS}")
    except Exception as e:
        print(f"❌ Failed to update .vscode settings: {e}")

def main():
    print("📦 Bootstrapping environment...")
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"✔ Already installed: {pkg}")
        except ImportError:
            print(f"➕ Installing missing package: {pkg}")
            install(pkg)

    patch_vscode_paths()

if __name__ == "__main__":
    main()
