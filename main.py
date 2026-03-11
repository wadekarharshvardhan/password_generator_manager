"""
main.py
-------
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Entry point of the application.
Bootstraps the PyQt6 application, shows the master password splash dialog,
and launches the main SecureVaultWindow upon successful authentication.

Run with:
    python main.py
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Import UI components
from ui import SecureVaultWindow, MasterPasswordDialog, STYLESHEET


def main():
    """
    Application entry point.
    1. Creates the QApplication instance.
    2. Applies the global dark cybersecurity stylesheet.
    3. Shows the master password prompt.
    4. Launches the main window if authentication succeeds.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("SecureVault")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SynthBay Solutions")
    app.setOrganizationDomain("synthbay.solutions")

    # Apply the global dark theme stylesheet to the entire application
    app.setStyleSheet(STYLESHEET)

    # ── Step 1: Master Password Dialog
    #    The user must enter a master password to unlock the vault.
    #    This password serves as the AES-256 encryption key derivation source.
    master_dialog = MasterPasswordDialog()
    result = master_dialog.exec()

    if result != MasterPasswordDialog.DialogCode.Accepted:
        # User cancelled the master password prompt — exit cleanly
        sys.exit(0)

    master_password = master_dialog.master_password

    # ── Step 2: Launch Main Application Window
    window = SecureVaultWindow(master_password=master_password)
    window.show()

    # ── Step 3: Run the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
