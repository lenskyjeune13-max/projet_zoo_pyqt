from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QDialogButtonBox, QMessageBox
)

class AnimalDialog(QDialog):
    def __init__(self, parent=None, animal=None):
        super().__init__(parent)
        self.animal = animal
        
        if animal:
            self.setWindowTitle("Modifier l'animal")
        else:
            self.setWindowTitle("Ajouter un animal")
            
        self.resize(350, 300)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        self.input_id = QLineEdit()
        self.input_nom = QLineEdit()
        self.input_espece = QLineEdit()
        self.input_age = QLineEdit()
        self.input_poids = QLineEdit()
        self.input_enclos = QLineEdit()
        
        self.combo_sante = QComboBox()
        self.combo_sante.addItems(["Bon", "Sous surveillance", "Malade"])
        
        form_layout.addRow("Identifiant:", self.input_id)
        form_layout.addRow("Nom:", self.input_nom)
        form_layout.addRow("Espece:", self.input_espece)
        form_layout.addRow("Age (ans):", self.input_age)
        form_layout.addRow("Poids (kg):", self.input_poids)
        form_layout.addRow("Enclos:", self.input_enclos)
        form_layout.addRow("Statut de sante:", self.combo_sante)
        
        layout.addLayout(form_layout)
        
        if animal:
            self.input_id.setText(str(animal.identifiant))
            self.input_id.setDisabled(True)
            self.input_nom.setText(str(animal.nom))
            self.input_espece.setText(str(animal.espece))
            self.input_age.setText(str(animal.age))
            self.input_poids.setText(str(animal.poids))
            self.input_enclos.setText(str(animal.enclos))
            self.combo_sante.setCurrentText(str(animal.statut_sante))
            
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.valider)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(self.button_box)

    def valider(self):
        if not self.input_id.text().strip() or not self.input_nom.text().strip():
            QMessageBox.warning(self, "Erreur", "L'identifiant et le nom ne peuvent pas etre vides.")
            return
        self.accept()

    def get_data(self):
        return {
            "identifiant": self.input_id.text().strip(),
            "nom": self.input_nom.text().strip(),
            "espece": self.input_espece.text().strip(),
            "age": self.input_age.text().strip(),
            "poids": self.input_poids.text().strip(),
            "enclos": self.input_enclos.text().strip(),
            "statut_sante": self.combo_sante.currentText()
        }