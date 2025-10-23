from subprocess import run, TimeoutExpired
from sys import executable
from os import getcwd
import platform

def install_tesseract():
    """
    Install Tesseract OCR based on the operating system.
    """
    system = platform.system().lower()
    
    if system == "windows":
        # Try different installation methods on Windows
        installers = [
            # Try winget first (Windows Package Manager)
            ['winget', 'install', 'UB-Mannheim.TesseractOCR'],
            # Try chocolatey if winget fails
            ['choco', 'install', 'tesseract'],
        ]
        
        for installer in installers:
            if installer[0] == 'winget':
                try:
                    print("🔧 Trying winget installation...")
                    # Use shell=True for Windows commands and proper error handling
                    result = run(
                        'winget install UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements',
                        shell=True,
                        capture_output=True, 
                        text=True, 
                        timeout=300,  # 5 minutes timeout
                        cwd=getcwd()
                    )
                    
                    print(f"Winget output: {result.stdout}")
                    if result.stderr:
                        print(f"Winget errors: {result.stderr}")
                    
                    if result.returncode == 0:
                        print("✅ Tesseract OCR installed successfully via winget!")
                        return True
                    else:
                        print("ℹ️  Tesseract may already be installed on your system. Please verify by running 'tesseract --version' in your command prompt/terminal.")
                        return False
                        
                except TimeoutExpired:
                    print("❌ Winget installation timed out")
                except Exception as e:
                    print(f"❌ Winget installation error: {e}")
            else:
                try:
                    print("🔧 Trying chocolatey installation...")
                    result = run(
                        'choco install tesseract -y',
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300,
                        cwd=getcwd()
                    )
                    
                    print(f"Chocolatey output: {result.stdout}")
                    if result.stderr:
                        print(f"Chocolatey errors: {result.stderr}")
                    
                    if result.returncode == 0:
                        print("✅ Tesseract OCR installed successfully via chocolatey!")
                        return True
                    else:
                        print(f"❌ Chocolatey installation failed with code: {result.returncode}")
                except TimeoutExpired:
                    print("❌ Chocolatey installation timed out")
                except Exception as e:
                    print(f"❌ Chocolatey installation error: {e}")

        
        print("❌ Automatic installation failed.")
        print("💡 Please install Tesseract manually:")
        print("   1. Run: winget install UB-Mannheim.TesseractOCR")
        print("   2. Or download from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
        
    elif system == "darwin":  # macOS
        try:
            print("🔧 Installing via Homebrew...")
            run(['brew', 'install', 'tesseract'], check=True)
            print("✅ Tesseract OCR installed successfully!")
            return True
        except:
            print("❌ Please install Homebrew first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
            
    elif system == "linux":
        try:
            print("🔧 Installing via apt...")
            run(['sudo', 'apt', 'update'], check=True)
            run(['sudo', 'apt', 'install', '-y', 'tesseract-ocr'], check=True)
            print("✅ Tesseract OCR installed successfully!")
            return True
        except:
            print("❌ Please install Tesseract manually: sudo apt install tesseract-ocr")
            return False
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def install_python_dependencies():
    """
    Install Python dependencies from requirements.txt
    """
    print("📦 Installing Python dependencies...")
    try:
        run([executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Python dependencies installed successfully!")
        return True
    except:
        print("❌ Failed to install Python dependencies")
        return False

def setup_project():
    """
    Complete project setup for new users.
    """
    print("🚀 Setting up WisprFlow Money Saver...")
    print("="*50)
    
    # Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Install Tesseract OCR
    if not install_tesseract():
        return False
    
    print("="*50)
    print("✅ Setup complete! You can now run the application.")
    print("💡 Run: python main.py")
    return True

if __name__ == "__main__":
    setup_project()