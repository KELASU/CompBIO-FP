from PyQt5 import QtWidgets, QtGui
import sys

class TumorSimulationUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.user_inputs = {}

    def init_ui(self):
        self.setWindowTitle("Tumor Growth Simulation")
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Initial Tumor Size
        self.initial_size_label = QtWidgets.QLabel("Initial Tumor Size (N0):")
        self.initial_size_input = QtWidgets.QLineEdit()
        layout.addWidget(self.initial_size_label)
        layout.addWidget(self.initial_size_input)

        # Growth Rate
        self.growth_rate_label = QtWidgets.QLabel("Growth Rate (r):")
        self.growth_rate_input = QtWidgets.QLineEdit()
        layout.addWidget(self.growth_rate_label)
        layout.addWidget(self.growth_rate_input)

        # Carrying Capacity
        self.carrying_capacity_label = QtWidgets.QLabel("Carrying Capacity (K):")
        self.carrying_capacity_input = QtWidgets.QLineEdit()
        layout.addWidget(self.carrying_capacity_label)
        layout.addWidget(self.carrying_capacity_input)

        # Temperature
        self.temperature_label = QtWidgets.QLabel("Temperature (°C):")
        self.temperature_input = QtWidgets.QLineEdit()
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.temperature_input)

        # Organ Selection
        self.organ_label = QtWidgets.QLabel("Select Organ:")
        self.organ_dropdown = QtWidgets.QComboBox()
        self.organ_dropdown.addItems(["Lungs", "Liver", "Brain"])
        layout.addWidget(self.organ_label)
        layout.addWidget(self.organ_dropdown)

        # Submit Button
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_inputs)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_inputs(self):
        self.user_inputs = {
            "N0": float(self.initial_size_input.text()),
            "r": float(self.growth_rate_input.text()),
            "K": float(self.carrying_capacity_input.text()),
            "temperature": float(self.temperature_input.text()),
            "organ": self.organ_dropdown.currentText(),
        }
        self.close()

    def get_inputs(self):
        return self.user_inputs

def get_user_inputs():
    app = QtWidgets.QApplication(sys.argv)
    ui = TumorSimulationUI()
    ui.show()
    app.exec_()
    return ui.get_inputs()
