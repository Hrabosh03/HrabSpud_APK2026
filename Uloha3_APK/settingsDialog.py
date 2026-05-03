from PyQt6 import QtWidgets

class settingsDialog(QtWidgets.QDialog):
    # Dialog for setting contour line parameters
    
    def __init__(self, dz, z_min, z_max):
        super().__init__()
        self.setWindowTitle("Nastavení parametrů")
        layout = QtWidgets.QFormLayout(self)
        
        self.dz_input = QtWidgets.QDoubleSpinBox()
        self.dz_input.setRange(0.1, 1000)
        self.dz_input.setValue(dz)
        
        self.z_min_input = QtWidgets.QDoubleSpinBox()
        self.z_min_input.setRange(-10000, 10000)
        self.z_min_input.setValue(z_min)
        
        self.z_max_input = QtWidgets.QDoubleSpinBox()
        self.z_max_input.setRange(-10000, 10000)
        self.z_max_input.setValue(z_max)
        
        layout.addRow("Krok vrstevnic (dz):", self.dz_input)
        layout.addRow("Minimální výška (z_min):", self.z_min_input)
        layout.addRow("Maximální výška (z_max):", self.z_max_input)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_values(self):
        # Return the values entered by the user
        return self.dz_input.value(), self.z_min_input.value(), self.z_max_input.value()