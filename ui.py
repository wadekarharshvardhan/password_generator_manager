"""
ui.py
-----
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Contribution: Chinmay Naik – PyQt6 User Interface Development Assistance
Internship Note: Chinmay Naik contributed to parts of the PyQt6 graphical
interface during his Python Development Internship at SynthBay Solutions
under the mentorship and technical guidance of Harshvardhan Wadekar.

This module defines the main application window and all UI components
using PyQt6. The interface features a modern dark cybersecurity theme.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QProgressBar,
    QGroupBox, QDialog, QDialogButtonBox, QFormLayout, QApplication,
    QSplitter, QStatusBar, QToolButton, QSizePolicy, QSpacerItem,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QClipboard,
    QLinearGradient, QPainter, QBrush, QPen, QFontDatabase,
)

from generator  import generate_password
from entropy    import calculate_entropy, get_strength_label, get_crack_time_estimate, get_strength_color
from encryption import encrypt_password, decrypt_password
from database   import initialize_database, save_entry, fetch_all_entries, delete_entry, search_entries, get_total_count


# ─────────────────────────────────────────────────────────────────────────────
#  STYLE CONSTANTS  (dark cybersecurity theme)
# ─────────────────────────────────────────────────────────────────────────────
STYLESHEET = """
/* ── Global App Background ── */
QMainWindow, QWidget {
    background-color: #0D1117;
    color: #E6EDF3;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}

/* ── Group Boxes ── */
QGroupBox {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    margin-top: 18px;
    padding: 14px 10px 10px 10px;
    color: #58A6FF;
    font-size: 13px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #58A6FF;
    font-size: 13px;
    font-weight: bold;
}

/* ── Input Fields ── */
QLineEdit {
    background-color: #21262D;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 9px 12px;
    color: #C9D1D9;
    font-size: 13px;
    selection-background-color: #1F6FEB;
}
QLineEdit:focus {
    border: 1px solid #58A6FF;
    background-color: #1C2128;
}
QLineEdit:hover {
    border: 1px solid #444C56;
}

/* ── Primary Buttons ── */
QPushButton {
    background-color: #21262D;
    color: #C9D1D9;
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #30363D;
    border-color: #58A6FF;
    color: #58A6FF;
}
QPushButton:pressed {
    background-color: #1F6FEB;
    color: #FFFFFF;
    border-color: #1F6FEB;
}
QPushButton:disabled {
    background-color: #161B22;
    color: #484F58;
    border-color: #21262D;
}

/* ── Accent Buttons ── */
QPushButton#btn_generate {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1F6FEB, stop:1 #0D419D);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 700;
}
QPushButton#btn_generate:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #388BFD, stop:1 #1F6FEB);
}

QPushButton#btn_save {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #238636, stop:1 #196C2E);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 700;
}
QPushButton#btn_save:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2EA043, stop:1 #238636);
}

QPushButton#btn_delete {
    background-color: #3D1F1F;
    color: #FF7B72;
    border: 1px solid #6E3030;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
}
QPushButton#btn_delete:hover {
    background-color: #6E3030;
    color: #FF7B72;
}

/* ── Slider ── */
QSlider::groove:horizontal {
    height: 6px;
    background: #21262D;
    border-radius: 3px;
    border: 1px solid #30363D;
}
QSlider::handle:horizontal {
    background: #58A6FF;
    border: 2px solid #1F6FEB;
    width: 18px;
    height: 18px;
    border-radius: 9px;
    margin: -6px 0;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1F6FEB, stop:1 #58A6FF);
    border-radius: 3px;
}

/* ── Checkboxes ── */
QCheckBox {
    color: #8B949E;
    font-size: 12px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #444C56;
    background-color: #21262D;
}
QCheckBox::indicator:checked {
    background-color: #1F6FEB;
    border-color: #58A6FF;
}
QCheckBox:hover {
    color: #C9D1D9;
}

/* ── Progress Bar (Strength Meter) ── */
QProgressBar {
    background-color: #21262D;
    border: 1px solid #30363D;
    border-radius: 5px;
    height: 10px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    border-radius: 5px;
}

/* ── Table ── */
QTableWidget {
    background-color: #161B22;
    gridline-color: #21262D;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #C9D1D9;
    font-size: 12px;
    alternate-background-color: #1C2128;
}
QTableWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #21262D;
}
QTableWidget::item:selected {
    background-color: #1F6FEB;
    color: #FFFFFF;
}
QHeaderView::section {
    background-color: #21262D;
    color: #58A6FF;
    border: none;
    border-bottom: 2px solid #1F6FEB;
    padding: 8px 10px;
    font-weight: bold;
    font-size: 12px;
}

/* ── Scroll Bars ── */
QScrollBar:vertical {
    background: #0D1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #30363D;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #58A6FF;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

/* ── Status Bar ── */
QStatusBar {
    background-color: #161B22;
    color: #8B949E;
    border-top: 1px solid #30363D;
    font-size: 12px;
}

/* ── Dialogs ── */
QDialog {
    background-color: #161B22;
}
QDialogButtonBox QPushButton {
    min-width: 80px;
}

/* ── Tool Buttons ── */
QToolButton {
    background-color: transparent;
    border: none;
    color: #8B949E;
    font-size: 16px;
}
QToolButton:hover {
    color: #58A6FF;
}

/* ── Frame separators ── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #30363D;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
#  MASTER PASSWORD DIALOG
# ─────────────────────────────────────────────────────────────────────────────
class MasterPasswordDialog(QDialog):
    """
    Splash dialog that prompts the user to enter a master password
    before the main vault window opens. The master password is used
    as the encryption/decryption key for all stored passwords.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SecureVault – Master Password")
        self.setFixedSize(420, 280)
        self.setModal(True)
        self.master_password: str = ""
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)

        # ── Logo / Title
        title = QLabel("🔐  SecureVault")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #58A6FF; letter-spacing: 1px;")
        layout.addWidget(title)

        subtitle = QLabel("Enter your Master Password to unlock the vault")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 12px; color: #8B949E; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        # ── Password Field
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Master Password")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.returnPressed.connect(self.accept)
        layout.addWidget(self.password_field)

        # ── Show/Hide toggle
        self.show_check = QCheckBox("Show password")
        self.show_check.stateChanged.connect(self._toggle_visibility)
        layout.addWidget(self.show_check)

        # ── Buttons
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        # Warning note
        note = QLabel("⚠  Remember your master password — it cannot be recovered.")
        note.setWordWrap(True)
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("font-size: 11px; color: #FFA502;")
        layout.addWidget(note)

    def _toggle_visibility(self, state):
        """Toggle echo mode for the master password field."""
        if state == Qt.CheckState.Checked.value:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

    def accept(self):
        """Validate and accept the master password."""
        pwd = self.password_field.text().strip()
        if len(pwd) < 6:
            QMessageBox.warning(self, "Too Short", "Master password must be at least 6 characters.")
            return
        self.master_password = pwd
        super().accept()


# ─────────────────────────────────────────────────────────────────────────────
#  DECRYPT VIEW DIALOG
# ─────────────────────────────────────────────────────────────────────────────
class DecryptDialog(QDialog):
    """
    Dialog displayed when the user clicks 'View' on a vault entry.
    Decrypts and shows the stored password for the selected record.
    """

    def __init__(self, encrypted_pass: str, master_password: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SecureVault – View Password")
        self.setFixedSize(380, 200)
        self.encrypted_pass = encrypted_pass
        self.master_password = master_password
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        label = QLabel("🔓  Decrypted Password")
        label.setStyleSheet("font-size: 15px; font-weight: bold; color: #58A6FF;")
        layout.addWidget(label)

        try:
            plain = decrypt_password(self.encrypted_pass, self.master_password)
        except ValueError as e:
            plain = f"Error: {e}"

        self.pass_field = QLineEdit(plain)
        self.pass_field.setReadOnly(True)
        self.pass_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pass_field)

        row = QHBoxLayout()
        show_btn = QPushButton("👁  Show")
        show_btn.setCheckable(True)
        show_btn.toggled.connect(self._toggle)
        copy_btn = QPushButton("📋  Copy")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(plain))
        row.addWidget(show_btn)
        row.addWidget(copy_btn)
        layout.addLayout(row)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _toggle(self, checked: bool):
        if checked:
            self.pass_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_field.setEchoMode(QLineEdit.EchoMode.Password)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class SecureVaultWindow(QMainWindow):
    """
    Main application window for SecureVault.
    Provides the complete UI for generating, evaluating, and managing passwords.
    """

    def __init__(self, master_password: str):
        super().__init__()
        self.master_password = master_password
        self.current_password: str = ""
        self.password_hidden: bool = True

        # Initialize database on startup
        initialize_database()

        self.setWindowTitle("🔐  SecureVault – Advanced Password Manager  |  SynthBay Solutions")
        self.setMinimumSize(1100, 720)
        self.resize(1200, 780)

        self._build_ui()
        self._refresh_table()
        self._update_status()

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  BUILD MAIN UI LAYOUT
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_ui(self):
        """Assemble all widgets into the main window layout."""
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setSpacing(0)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ── Top Header Banner
        root_layout.addWidget(self._build_header())

        # ── Main content area (split: left controls | right vault table)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: #30363D; width: 1px; }")

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([520, 680])  # Initial split ratio

        root_layout.addWidget(splitter, stretch=1)

        # ── Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🔒  Vault locked and secure  |  SynthBay Solutions")

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  HEADER BANNER
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_header(self) -> QWidget:
        """Build the top gradient header banner with title and branding."""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0D1117, stop:0.4 #161B22, stop:1 #0D419D);
                border-bottom: 2px solid #1F6FEB;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        title_lbl = QLabel("🔐  SecureVault")
        title_lbl.setStyleSheet("font-size: 22px; font-weight: 800; color: #58A6FF; letter-spacing: 2px;")

        brand_lbl = QLabel("SynthBay Solutions  ·  Advanced Password Manager")
        brand_lbl.setStyleSheet("font-size: 12px; color: #8B949E;")
        brand_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(title_lbl)
        layout.addStretch()
        layout.addWidget(brand_lbl)
        return header

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  LEFT PANEL  (generator + entry form)
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_left_panel(self) -> QWidget:
        """Build the left panel containing password generator and save form."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 8, 16)

        layout.addWidget(self._build_generator_group())
        layout.addWidget(self._build_strength_group())
        layout.addWidget(self._build_entry_form_group())
        layout.addStretch()

        return panel

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  PASSWORD GENERATOR GROUP
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_generator_group(self) -> QGroupBox:
        """Password generator controls: character options, length, output."""
        group = QGroupBox("⚡  Password Generator")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        # ── Character Type Checkboxes
        check_row = QHBoxLayout()
        self.cb_upper   = QCheckBox("A–Z  Uppercase")
        self.cb_lower   = QCheckBox("a–z  Lowercase")
        self.cb_digits  = QCheckBox("0–9  Digits")
        self.cb_symbols = QCheckBox("!@#  Symbols")

        for cb in (self.cb_upper, self.cb_lower, self.cb_digits, self.cb_symbols):
            cb.setChecked(True)
            check_row.addWidget(cb)

        layout.addLayout(check_row)

        # ── Length Slider
        length_row = QHBoxLayout()
        length_label = QLabel("Length:")
        length_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(64)
        self.length_slider.setValue(16)
        self.length_slider.setTickInterval(8)
        self.length_slider.valueChanged.connect(self._on_length_changed)

        self.length_display = QLabel("16")
        self.length_display.setFixedWidth(36)
        self.length_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_display.setStyleSheet(
            "color: #58A6FF; font-weight: bold; font-size: 14px;"
            "background: #21262D; border-radius: 6px; padding: 2px 4px;"
        )

        length_row.addWidget(length_label)
        length_row.addWidget(self.length_slider, stretch=1)
        length_row.addWidget(self.length_display)
        layout.addLayout(length_row)

        # ── Password Output Field
        output_row = QHBoxLayout()
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Click 'Generate' to create a password…")
        self.password_field.setReadOnly(True)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setStyleSheet(
            "font-family: 'Consolas', 'Courier New', monospace; font-size: 14px;"
            "letter-spacing: 2px; color: #2ED573; background-color: #1C2128;"
            "border: 1px solid #238636; border-radius: 8px; padding: 10px 14px;"
        )

        # Show/Hide toggle button
        self.toggle_btn = QToolButton()
        self.toggle_btn.setText("👁")
        self.toggle_btn.setToolTip("Toggle password visibility")
        self.toggle_btn.clicked.connect(self._toggle_password_visibility)
        self.toggle_btn.setFixedSize(36, 36)
        self.toggle_btn.setStyleSheet(
            "QToolButton { background:#21262D; border:1px solid #30363D; border-radius:8px; font-size:16px; }"
            "QToolButton:hover { border-color:#58A6FF; }"
        )

        # Copy button
        copy_btn = QPushButton("📋")
        copy_btn.setToolTip("Copy password to clipboard")
        copy_btn.setFixedSize(36, 36)
        copy_btn.clicked.connect(self._copy_to_clipboard)
        copy_btn.setStyleSheet(
            "QPushButton { background:#21262D; border:1px solid #30363D; border-radius:8px; font-size:16px; }"
            "QPushButton:hover { border-color:#58A6FF; }"
        )

        output_row.addWidget(self.password_field, stretch=1)
        output_row.addWidget(self.toggle_btn)
        output_row.addWidget(copy_btn)
        layout.addLayout(output_row)

        # ── Generate Button
        self.btn_generate = QPushButton("⚡  Generate Secure Password")
        self.btn_generate.setObjectName("btn_generate")
        self.btn_generate.setMinimumHeight(42)
        self.btn_generate.clicked.connect(self._generate_password)
        layout.addWidget(self.btn_generate)

        return group

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  PASSWORD STRENGTH GROUP
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_strength_group(self) -> QGroupBox:
        """Strength indicator: progress bar, entropy, crack-time labels."""
        group = QGroupBox("📊  Password Strength Analysis")
        layout = QGridLayout(group)
        layout.setSpacing(10)
        layout.setColumnStretch(1, 1)

        # Strength Label + Bar
        layout.addWidget(QLabel("Strength:"),      0, 0)
        self.strength_label = QLabel("—")
        self.strength_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #8B949E;")
        layout.addWidget(self.strength_label,      0, 1)

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setFixedHeight(12)
        self.strength_bar.setTextVisible(False)
        layout.addWidget(self.strength_bar,        1, 0, 1, 2)

        # Entropy
        layout.addWidget(QLabel("Entropy:"),       2, 0)
        self.entropy_label = QLabel("0.00 bits")
        self.entropy_label.setStyleSheet("color: #FFA502; font-weight: bold;")
        layout.addWidget(self.entropy_label,       2, 1)

        # Crack Time Estimate
        layout.addWidget(QLabel("Crack Resistance:"), 3, 0)
        self.crack_label = QLabel("—")
        self.crack_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.crack_label.setWordWrap(True)
        layout.addWidget(self.crack_label,         3, 1)

        return group

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  ENTRY FORM GROUP (Website + Username + Save)
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_entry_form_group(self) -> QGroupBox:
        """Website and username input fields + Save to Vault button."""
        group = QGroupBox("💾  Save to Vault")
        layout = QFormLayout(group)
        layout.setSpacing(10)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.website_field = QLineEdit()
        self.website_field.setPlaceholderText("e.g. github.com")

        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("e.g. user@email.com")

        layout.addRow("Website:", self.website_field)
        layout.addRow("Username:", self.username_field)

        self.btn_save = QPushButton("🔒  Save Encrypted Password")
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setMinimumHeight(42)
        self.btn_save.clicked.connect(self._save_password)

        # Wrap the button in a plain layout (FormLayout doesn't span well)
        btn_widget = QWidget()
        btn_layout = QVBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 4, 0, 0)
        btn_layout.addWidget(self.btn_save)
        layout.addRow(btn_widget)

        return group

    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    #  RIGHT PANEL  (vault table)
    # ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
    def _build_right_panel(self) -> QWidget:
        """Build the right panel with a searchable table of vault entries."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(8, 16, 16, 16)

        # ── Header row (title + search bar)
        header_row = QHBoxLayout()

        vault_title = QLabel("🗄  Password Vault")
        vault_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #58A6FF;")

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍  Search by website or username…")
        self.search_field.setFixedWidth(260)
        self.search_field.textChanged.connect(self._filter_table)

        refresh_btn = QPushButton("↻")
        refresh_btn.setToolTip("Refresh vault")
        refresh_btn.setFixedSize(34, 34)
        refresh_btn.clicked.connect(self._refresh_table)
        refresh_btn.setStyleSheet(
            "QPushButton { background:#21262D; border:1px solid #30363D; border-radius:8px; font-size:16px; }"
            "QPushButton:hover { border-color:#58A6FF; color:#58A6FF; }"
        )

        header_row.addWidget(vault_title)
        header_row.addStretch()
        header_row.addWidget(self.search_field)
        header_row.addWidget(refresh_btn)
        layout.addLayout(header_row)

        # ── Vault Table
        self.vault_table = QTableWidget()
        self.vault_table.setColumnCount(5)
        self.vault_table.setHorizontalHeaderLabels(
            ["#", "Website", "Username", "Date Created", "Actions"]
        )
        self.vault_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.vault_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.vault_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.vault_table.setColumnWidth(0, 40)
        self.vault_table.setColumnWidth(4, 160)
        self.vault_table.verticalHeader().setVisible(False)
        self.vault_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.vault_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.vault_table.setAlternatingRowColors(True)
        self.vault_table.setShowGrid(False)
        self.vault_table.setWordWrap(False)
        layout.addWidget(self.vault_table, stretch=1)

        # ── Footer with entry count
        self.entry_count_label = QLabel("0 entries stored")
        self.entry_count_label.setStyleSheet("font-size: 11px; color: #8B949E;")
        layout.addWidget(self.entry_count_label)

        return panel

    # ─────────────────────────────────────────────────────────────────────────
    #  SLOT HANDLERS
    # ─────────────────────────────────────────────────────────────────────────

    def _on_length_changed(self, value: int):
        """Update the length display label when the slider moves."""
        self.length_display.setText(str(value))

    def _generate_password(self):
        """Generate a new secure password and update UI metrics."""
        try:
            pwd = generate_password(
                length=self.length_slider.value(),
                use_uppercase=self.cb_upper.isChecked(),
                use_lowercase=self.cb_lower.isChecked(),
                use_digits=self.cb_digits.isChecked(),
                use_symbols=self.cb_symbols.isChecked(),
            )
            self.current_password = pwd
            self.password_field.setText(pwd)
            # Always start new password in hidden mode
            self.password_hidden = True
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("👁")
            self._update_strength_display(pwd)
            self._flash_generate_button()
        except ValueError as err:
            QMessageBox.warning(self, "Generation Error", str(err))

    def _update_strength_display(self, password: str):
        """Recalculate and display entropy, strength bar, and crack time."""
        entropy = calculate_entropy(password)
        label   = get_strength_label(entropy)
        color   = get_strength_color(label)
        crack   = get_crack_time_estimate(entropy)

        self.entropy_label.setText(f"{entropy:.2f} bits")
        self.strength_label.setText(label)
        self.strength_label.setStyleSheet(f"font-weight: bold; font-size: 13px; color: {color};")
        self.crack_label.setText(crack)

        # Map strength label to progress bar value (0–100)
        bar_map = {"Weak": 25, "Medium": 50, "Strong": 75, "Very Strong": 100}
        bar_val = bar_map.get(label, 0)
        self.strength_bar.setValue(bar_val)
        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background: {color}; border-radius: 5px; }}"
        )

    def _toggle_password_visibility(self):
        """Toggle the echo mode on the password output field."""
        if self.password_hidden:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setText("🙈")
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setText("👁")
        self.password_hidden = not self.password_hidden

    def _copy_to_clipboard(self):
        """Copy the currently generated password to the system clipboard."""
        if not self.current_password:
            self.status_bar.showMessage("⚠  No password to copy. Generate one first.", 3000)
            return
        QApplication.clipboard().setText(self.current_password)
        self.status_bar.showMessage("✅  Password copied to clipboard!", 3000)

    def _save_password(self):
        """Encrypt and store the current password entry to the vault."""
        website  = self.website_field.text().strip()
        username = self.username_field.text().strip()
        password = self.current_password

        # Input validation
        if not website:
            QMessageBox.warning(self, "Missing Field", "Please enter a website or service name.")
            return
        if not username:
            QMessageBox.warning(self, "Missing Field", "Please enter a username or email.")
            return
        if not password:
            QMessageBox.warning(self, "No Password", "Please generate a password first.")
            return

        try:
            encrypted = encrypt_password(password, self.master_password)
            save_entry(website, username, encrypted)
            self._refresh_table()
            self._update_status()

            # Reset fields after successful save
            self.website_field.clear()
            self.username_field.clear()
            self.status_bar.showMessage(
                f"✅  Password for '{website}' saved securely (AES-256 encrypted).", 5000
            )
        except Exception as err:
            QMessageBox.critical(self, "Save Error", f"Failed to save entry:\n{err}")

    def _refresh_table(self):
        """Reload all entries from the database into the vault table."""
        keyword = self.search_field.text().strip()
        if keyword:
            entries = search_entries(keyword)
        else:
            entries = fetch_all_entries()

        self._populate_table(entries)

    def _filter_table(self):
        """Live search: re-query database as user types in the search field."""
        self._refresh_table()

    def _populate_table(self, entries: list):
        """Fill the vault table widget with a list of entry tuples."""
        self.vault_table.setRowCount(0)  # Clear current rows

        for row_idx, (entry_id, website, username, encrypted_pass, date_created) in enumerate(entries):
            self.vault_table.insertRow(row_idx)

            # Row number (display only)
            id_item = QTableWidgetItem(str(row_idx + 1))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setForeground(QColor("#484F58"))
            self.vault_table.setItem(row_idx, 0, id_item)

            # Website
            site_item = QTableWidgetItem(website)
            site_item.setForeground(QColor("#58A6FF"))
            self.vault_table.setItem(row_idx, 1, site_item)

            # Username
            self.vault_table.setItem(row_idx, 2, QTableWidgetItem(username))

            # Date Created
            date_item = QTableWidgetItem(date_created)
            date_item.setForeground(QColor("#8B949E"))
            self.vault_table.setItem(row_idx, 3, date_item)

            # Action Buttons (View + Delete) embedded in the cell
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(6)

            view_btn = QPushButton("🔓  View")
            view_btn.setFixedHeight(26)
            view_btn.setStyleSheet(
                "QPushButton { background:#21262D; border:1px solid #30363D; border-radius:5px; "
                "color:#C9D1D9; font-size:11px; padding:2px 8px; }"
                "QPushButton:hover { border-color:#58A6FF; color:#58A6FF; }"
            )
            # Capture entry_id in closure using default argument
            view_btn.clicked.connect(lambda _, eid=entry_id, ep=encrypted_pass: self._view_entry(eid, ep))

            del_btn = QPushButton("🗑")
            del_btn.setObjectName("btn_delete")
            del_btn.setFixedHeight(26)
            del_btn.clicked.connect(lambda _, eid=entry_id, site=website: self._delete_entry(eid, site))

            action_layout.addWidget(view_btn)
            action_layout.addWidget(del_btn)
            self.vault_table.setCellWidget(row_idx, 4, action_widget)
            self.vault_table.setRowHeight(row_idx, 40)

        self.entry_count_label.setText(f"{len(entries)} entr{'y' if len(entries)==1 else 'ies'} stored")

    def _view_entry(self, entry_id: int, encrypted_pass: str):
        """Open the decrypt dialog for a selected vault entry."""
        dlg = DecryptDialog(encrypted_pass, self.master_password, self)
        dlg.exec()

    def _delete_entry(self, entry_id: int, website: str):
        """Prompt and delete a vault entry after user confirmation."""
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the entry for\n'{website}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            delete_entry(entry_id)
            self._refresh_table()
            self._update_status()
            self.status_bar.showMessage(f"🗑  Entry for '{website}' deleted.", 3000)

    def _update_status(self):
        """Refresh the status bar with the current vault entry count."""
        count = get_total_count()
        self.status_bar.showMessage(
            f"🔒  Vault secured  ·  {count} password{'s' if count != 1 else ''} stored  ·  AES-256 Encrypted  ·  SynthBay Solutions"
        )

    def _flash_generate_button(self):
        """Briefly highlight the generate button to provide visual feedback."""
        original_style = self.btn_generate.styleSheet()
        self.btn_generate.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 #2EA043, stop:1 #238636); color:#fff; border:none; border-radius:8px; "
            "padding:10px 20px; font-size:14px; font-weight:700;"
        )
        QTimer.singleShot(400, lambda: self.btn_generate.setStyleSheet(original_style))
