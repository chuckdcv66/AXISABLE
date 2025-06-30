import subprocess
import sys

REQUIRED_PACKAGES = [
    "PyQt5",
    "PyQtWebEngine"
]

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package}")

def main():
    print("📦 Bootstrapping required packages...")
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"✔ Already installed: {pkg}")
        except ImportError:
            print(f"➕ Missing: {pkg} → installing...")
            install(pkg)

if __name__ == "__main__":
    main()
