from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFrame, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from theme import Theme


class LoginDialog(QDialog):
    """Login dialog for authentication before accessing the dashboard."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.authenticated = False
        
        self.setWindowTitle("Login - Chemical Equipment Analytics Dashboard")
        self.setFixedSize(440, 500)
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        # Set base background
        self.setStyleSheet(f"background-color: {Theme.BACKGROUND};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(12)
        
        # Spacer at top
        layout.addSpacing(10)
        
        # Logo Circle
        logo_container = QWidget()
        logo_container.setFixedSize(80, 80)
        logo_container.setStyleSheet(f"""
            background-color: {Theme.PRIMARY};
            border-radius: 40px;
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_text = QLabel("🔒")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_text.setStyleSheet("font-size: 32px; background: transparent;")
        logo_layout.addWidget(logo_text)
        
        # Center logo
        logo_row = QHBoxLayout()
        logo_row.addStretch()
        logo_row.addWidget(logo_container)
        logo_row.addStretch()
        layout.addLayout(logo_row)
        
        layout.addSpacing(20)
        
        # Title - explicit dark color
        title_label = QLabel("Welcome Back")
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont("Segoe UI", 22)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #171717; background: transparent;")
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Sign in to access the Analytics Dashboard")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #707070; font-size: 13px; background: transparent;")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(25)
        
        # Username label
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #171717; font-weight: bold; font-size: 13px; background: transparent;")
        layout.addWidget(username_label)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(44)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #f6f6f6;
                color: #171717;
                border: 1px solid #dfdfdf;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {Theme.PRIMARY};
            }}
        """)
        layout.addWidget(self.username_input)
        
        layout.addSpacing(8)
        
        # Password label
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #171717; font-weight: bold; font-size: 13px; background: transparent;")
        layout.addWidget(password_label)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(44)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #f6f6f6;
                color: #171717;
                border: 1px solid #dfdfdf;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {Theme.PRIMARY};
            }}
        """)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(25)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: #1e2723;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #5fd69a;
            }}
            QPushButton:pressed {{
                background-color: #4bc98a;
            }}
        """)
        self.login_btn.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_btn)
        
        # Connect Enter key
        self.password_input.returnPressed.connect(self.attempt_login)
        self.username_input.returnPressed.connect(self.focus_password)
        
        layout.addStretch()
        
    def focus_password(self):
        self.password_input.setFocus()
        
    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Please enter both username and password.")
            return
        
        self.login_btn.setText("Logging in...")
        self.login_btn.setEnabled(False)
        
        try:
            self.api_client.set_credentials(username, password)
            
            if self.api_client.test_auth():
                self.authenticated = True
                self.accept()
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
                self.api_client.clear_credentials()
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect to server:\n{str(e)}")
            self.api_client.clear_credentials()
        finally:
            self.login_btn.setText("Login")
            self.login_btn.setEnabled(True)
    
    def get_credentials(self):
        return (self.username_input.text().strip(), self.password_input.text())
