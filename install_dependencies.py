import subprocess
import os

def create_virtualenv():
    if os.path.isdir("env"):
        print("Virtual environment 'env' already exists.")
        return
    
    try:
        print("Creating virtual environment...")
        subprocess.run(["python", "-m", "venv", "env"], check=True)
        print("Virtual environment created successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to create virtual environment.")
    except Exception as e:
        print(f"Error: {e}")

def install_dependencies():
    try:
        print("Installing dependencies...")
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("All Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
    except Exception as e:
        print(f"Error: {e}")

def activate_virtualenv():
    try:
        print("Activating virtual environment...")
        activate_script = os.path.join("env", "Scripts", "activate.bat")
        subprocess.run(f"call {activate_script}", shell=True, check=True)
        print("Virtual environment activated successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to activate virtual environment.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_virtualenv()
    activate_virtualenv()
    install_dependencies()
    print("Requirements already satisfied.")
