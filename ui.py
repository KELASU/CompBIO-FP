from PyQt5 import QtWidgets, QtCore


class TumorSimulationUI(QtWidgets.QWidget):
    def __init__(self, tumor_types):
        super().__init__()
        self.tumor_types = tumor_types
        self.init_ui()
        self.user_inputs = {}

    def init_ui(self):
        self.setWindowTitle("Tumor Growth Simulation")
        self.setGeometry(100, 100, 400, 500)

        layout = QtWidgets.QVBoxLayout()

        self.initial_size_label = QtWidgets.QLabel("Initial Tumor Size (N0):")
        self.initial_size_input = QtWidgets.QLineEdit()
        layout.addWidget(self.initial_size_label)
        layout.addWidget(self.initial_size_input)

        self.age_label = QtWidgets.QLabel("Age of Patient:")
        self.age_input = QtWidgets.QLineEdit()
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        self.growth_rate_label = QtWidgets.QLabel("Growth Rate (r):")
        self.growth_rate_input = QtWidgets.QLineEdit()
        layout.addWidget(self.growth_rate_label)
        layout.addWidget(self.growth_rate_input)

        self.organ_label = QtWidgets.QLabel("Select Organ:")
        self.organ_dropdown = QtWidgets.QComboBox()
        self.organ_dropdown.addItems(self.tumor_types.keys())
        self.organ_dropdown.currentTextChanged.connect(self.update_tumor_types)
        layout.addWidget(self.organ_label)
        layout.addWidget(self.organ_dropdown)

        self.tumor_type_label = QtWidgets.QLabel("Select Tumor Type:")
        self.tumor_dropdown = QtWidgets.QComboBox()
        layout.addWidget(self.tumor_type_label)
        layout.addWidget(self.tumor_dropdown)

        self.model_label = QtWidgets.QLabel("Select Growth Model:")
        layout.addWidget(self.model_label)

        self.model_group = QtWidgets.QButtonGroup(self)
        self.gompertz_radio = QtWidgets.QRadioButton("Gompertz")
        self.logistic_radio = QtWidgets.QRadioButton("Logistic")
        self.gompertz_radio.setChecked(True)  # Default selection
        self.model_group.addButton(self.gompertz_radio)
        self.model_group.addButton(self.logistic_radio)

        layout.addWidget(self.gompertz_radio)
        layout.addWidget(self.logistic_radio)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_inputs)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.update_tumor_types()

    def update_tumor_types(self):
        organ = self.organ_dropdown.currentText()
        self.tumor_dropdown.clear()
        if organ in self.tumor_types:
            self.tumor_dropdown.addItems(self.tumor_types[organ].keys())

    def submit_inputs(self):
        try:
            selected_model = "Gompertz" if self.gompertz_radio.isChecked() else "Logistic"
            self.user_inputs = {
                "N0": float(self.initial_size_input.text()),
                "age": int(self.age_input.text()),
                "r": float(self.growth_rate_input.text()),
                "organ": self.organ_dropdown.currentText(),
                "tumor_type": self.tumor_dropdown.currentText(),
                "growth_model": selected_model,
            }
            self.close()
        except ValueError:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Invalid input. Please check your entries.")

    def get_inputs(self):
        return self.user_inputs


def get_user_inputs(tumor_types):
    app = QtWidgets.QApplication([])
    ui = TumorSimulationUI(tumor_types)
    ui.show()
    app.exec_()
    return ui.get_inputs()
