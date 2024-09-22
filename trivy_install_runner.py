import os
import platform
import subprocess
import sys
import argparse

# Function to parse command-line arguments (without --version flag)
def parse_arguments():
    parser = argparse.ArgumentParser(description="Install Trivy by specifying the version.")
    parser.add_argument(
        "version",  # Positional argument
        type=str,
        help="Specify the Trivy version to install (e.g., 0.53.0)."
    )
    args = parser.parse_args()
    return args.version

# Function to check if Trivy is already installed
def is_trivy_installed():
    try:
        result = subprocess.run(["trivy", "--version"], check=True, capture_output=True, text=True)
        installed_version = result.stdout.split()[1].lstrip('v')
        print(f"Trivy is already installed (version: {installed_version}). Skipping installation.")
        return True
    except subprocess.CalledProcessError:
        print("Trivy is not installed.")
        return False

# Function to check the OS, architecture, set the download URL, and install the package
def install_trivy(trivy_version):
    # Detect the OS
    os_name = platform.system().lower()

    if os_name == "linux":
        # Check for specific Linux distribution
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                os_release = f.read()

            # Check for CPU architecture
            arch = platform.machine()
            if arch == "x86_64":
                arch_type = "64bit"
            elif arch == "aarch64":
                arch_type = "ARM64"
            else:
                print(f"Unsupported architecture: {arch}")
                sys.exit(1)

            if "amazon linux" in os_release.lower():
                print(f"Amazon Linux detected, architecture: {arch}")
                # Set download URL for Amazon Linux
                download_url = f"https://github.com/aquasecurity/trivy/releases/download/v{trivy_version}/trivy_{trivy_version}_Linux-{arch_type}.rpm"

                # Call bash commands for Amazon Linux
                execute_bash_commands("rpm", arch_type, download_url, trivy_version)
            elif "ubuntu" in os_release.lower():
                print(f"Ubuntu detected, architecture: {arch}")
                # Set download URL for Ubuntu
                download_url = f"https://github.com/aquasecurity/trivy/releases/download/v{trivy_version}/trivy_{trivy_version}_Linux-{arch_type}.deb"

                # Call bash commands for Ubuntu
                execute_bash_commands("deb", arch_type, download_url, trivy_version)
            else:
                print("Unsupported Linux distribution.")
                sys.exit(1)
        else:
            print("/etc/os-release not found. Unsupported Linux distribution.")
            sys.exit(1)
    else:
        print(f"Unsupported OS: {os_name}")
        sys.exit(1)

# Function to execute bash commands based on the package type, architecture, and download URL
def execute_bash_commands(package_type, arch_type, download_url, trivy_version):
    try:
        # Download the package using curl
        print(f"Downloading Trivy {package_type.upper()} package from {download_url}...")
        subprocess.run(["curl", "-LO", download_url], check=True)

        # Install the package based on the type (rpm or deb)
        if package_type == "rpm":
            print("Installing Trivy RPM package...")
            subprocess.run(["sudo", "rpm", "-ivh", f"trivy_{trivy_version}_Linux-{arch_type}.rpm"], check=True)
            os.remove(f"trivy_{trivy_version}_Linux-{arch_type}.rpm")
        elif package_type == "deb":
            print("Installing Trivy DEB package...")
            subprocess.run(["sudo", "dpkg", "-i", f"trivy_{trivy_version}_Linux-{arch_type}.deb"], check=True)
            os.remove(f"trivy_{trivy_version}_Linux-{arch_type}.deb")

        print("Trivy installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

# Function to verify if Trivy was installed successfully
def verify_installation():
    try:
        result = subprocess.run(["trivy", "--version"], check=True, capture_output=True, text=True)
        installed_version = result.stdout.split()[1].lstrip('v')
        print(f"Trivy installed successfully. Version: {installed_version}")
    except subprocess.CalledProcessError:
        print("Trivy installation failed or Trivy is not installed.")
        sys.exit(1)

if __name__ == "__main__":
    # Parse the version argument from the command line
    trivy_version = parse_arguments()

    # Check if Trivy is already installed
    if not is_trivy_installed():
        # Install Trivy if it's not installed
        install_trivy(trivy_version)

    # Verify the installation
    verify_installation()
