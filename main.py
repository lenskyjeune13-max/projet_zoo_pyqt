import sys
from PyQt6.QtWidgets import QApplication
from gestion_zoo import GestionZoo
from interface.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gestion = GestionZoo()
    fenetre = MainWindow(gestion)
    fenetre.show()
    sys.exit(app.exec())