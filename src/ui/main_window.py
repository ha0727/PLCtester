from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QGroupBox,
    QStatusBar
)
from src.ui.widgets.connection_dialog import ConnectionDialog
from src.plc.plc_client import PLCClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLC 사전 테스트 프로그램")
        self.setGeometry(100, 100, 600, 400)
        self.setStatusBar(QStatusBar())

        self.plc_client = PLCClient()

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout(central_widget)

        # Equipment Selection
        equipment_group = QGroupBox("장비 선택")
        equipment_layout = QHBoxLayout()
        equipment_label = QLabel("대상 장비 모델:")
        self.equipment_combo = QComboBox()
        self.equipment_combo.addItems(["장비 A", "장비 B", "장비 C"]) # Placeholder
        equipment_layout.addWidget(equipment_label)
        equipment_layout.addWidget(self.equipment_combo)
        equipment_group.setLayout(equipment_layout)
        main_layout.addWidget(equipment_group)

        # Scenario Type Selection
        scenario_group = QGroupBox("시나리오 타입 선택")
        scenario_layout = QHBoxLayout()
        self.common_button = QPushButton("Common")
        self.normal_button = QPushButton("Normal")
        self.abnormal_button = QPushButton("Abnormal")
        scenario_layout.addWidget(self.common_button)
        scenario_layout.addWidget(self.normal_button)
        scenario_layout.addWidget(self.abnormal_button)
        scenario_group.setLayout(scenario_layout)
        main_layout.addWidget(scenario_group)

        # Connection Settings
        connection_group = QGroupBox("연결 설정")
        connection_layout = QHBoxLayout()
        self.connection_button = QPushButton("연결 설정")
        self.connection_button.clicked.connect(self.toggle_connection)
        connection_layout.addWidget(self.connection_button)
        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)

        self.update_ui_for_connection_status(False) # Initial UI state

    def toggle_connection(self):
        if not self.plc_client.connected:
            dialog = ConnectionDialog(self)
            if dialog.exec():
                ip, port = dialog.get_connection_details()
                success, message = self.plc_client.connect(ip, port)
                self.statusBar().showMessage(message, 5000)
                self.update_ui_for_connection_status(success)
        else:
            self.plc_client.disconnect()
            self.statusBar().showMessage("PLC 연결이 해제되었습니다.", 5000)
            self.update_ui_for_connection_status(False)

    def update_ui_for_connection_status(self, connected):
        self.common_button.setEnabled(connected)
        self.normal_button.setEnabled(connected)
        self.abnormal_button.setEnabled(connected)
        self.equipment_combo.setEnabled(not connected)

        if connected:
            self.connection_button.setText("연결 해제")
            self.connection_button.setProperty("secondary", True)
        else:
            self.connection_button.setText("연결 설정")
            self.connection_button.setProperty("secondary", False)
        
        # Re-apply style to update property changes
        self.connection_button.style().polish(self.connection_button)
