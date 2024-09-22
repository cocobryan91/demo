Steps:

  verify_installation function:
      After attempting to install Trivy, this function checks if Trivy is installed correctly by running trivy --version. It outputs the installed version to confirm success.
      If Trivy is not installed or there’s a problem, it will print an error message and exit.

  Final Installation Check:
      After the script installs Trivy (if it wasn’t already installed), it verifies the installation and outputs the installed version to confirm that it worked.
