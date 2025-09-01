from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QLabel
)

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PLC 연결 설정")

        self.ip_address_edit = QLineEdit("127.0.0.1")
        self.port_edit = QLineEdit("102")

        # Create layout and add widgets
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        ip_label = QLabel("IP 주소:")
        ip_label.setProperty("class", "dialog-label")
        port_label = QLabel("포트:")
        port_label.setProperty("class", "dialog-label")

        form_layout.addRow(ip_label, self.ip_address_edit)
        form_layout.addRow(port_label, self.port_edit)
        
        layout.addLayout(form_layout)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(self.button_box)

    def get_connection_details(self):
        """Returns the entered IP address and port."""
        return self.ip_address_edit.text(), int(self.port_edit.text())
