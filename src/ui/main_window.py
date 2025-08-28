from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QGroupBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLC 사전 테스트 프로그램")
        self.setGeometry(100, 100, 600, 400)

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
        connection_layout.addWidget(self.connection_button)
        connection_group.setLayout(connection_layout)
        main_layout.addWidget(connection_group)