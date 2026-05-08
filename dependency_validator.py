import pkg_resources
import sys

REQUIRED_PACKAGES = {
    "tensorflow": "2.16.1",
    "mediapipe": None,
    "streamlit": None,
    "fastapi": None,
    "opencv-python-headless": None,
    "sqlalchemy": None
}

def validate_dependencies():
    print("Validating critical dependency versions...")
    all_ok = True
    
    for pkg, version in REQUIRED_PACKAGES.items():
        try:
            installed = pkg_resources.get_distribution(pkg)
            if version and installed.version != version:
                print(f"❌ {pkg}: Version mismatch. Required {version}, found {installed.version}")
                all_ok = False
            else:
                print(f"✅ {pkg}: {installed.version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {pkg}: NOT INSTALLED")
            all_ok = False
            
    return all_ok

if __name__ == "__main__":
    if validate_dependencies():
        print("\nAll critical dependencies validated successfully.")
        sys.exit(0)
    else:
        print("\nDependency validation failed. Please run 'pip install -r requirements.txt'")
        sys.exit(1)
