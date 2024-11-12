import subprocess
import sys

def install_requirements():
    # List of all dependencies required by the project
    requirements = [
        "ccxt",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "matplotlib",
        "talib",
        "requests",
        "logging"
    ]
    
    # Install each package using pip
    for package in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("[+] All dependencies have been installed successfully!")

if __name__ == "__main__":
    install_requirements()
