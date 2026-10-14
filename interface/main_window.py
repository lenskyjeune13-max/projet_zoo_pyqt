from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox,
    QTextEdit, QHeaderView, QFileDialog
)
from animal import Animal
from interface.animal_dialog import AnimalDialog


class MainWindow(QMainWindow):
    def __init__(self, gestion):
        super().__init__()
        # 'gestion' vini nan main.py: MainWindow(gestion)
        self.gestion = gestion

        self.setWindowTitle("Gestion de Zoo - Projet Python PyQt6")
        self.resize(900, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_animaux = QWidget()
        self.tab_stats = QWidget()

        self.tabs.addTab(self.tab_animaux, "Gestion des Animaux")
        self.tabs.addTab(self.tab_stats, "Statistiques et Analyses")

        self.init_tab_animaux()
        self.init_tab_stats()
        self.creer_menu()

        self.rafraichir_tableau()

    def init_tab_animaux(self):
        layout = QVBoxLayout(self.tab_animaux)

        layout_haut = QHBoxLayout()
        self.input_recherche = QLineEdit()
        self.input_recherche.setPlaceholderText("Rechercher par nom, espece ou ID...")
        self.input_recherche.textChanged.connect(self.rechercher_animaux)
        layout_haut.addWidget(QLabel("Recherche :"))
        layout_haut.addWidget(self.input_recherche)

        self.btn_trier_age = QPushButton("Trier par Age")
        self.btn_trier_age.clicked.connect(lambda: self.trier("age"))
        layout_haut.addWidget(self.btn_trier_age)

        self.btn_trier_poids = QPushButton("Trier par Poids")
        self.btn_trier_poids.clicked.connect(lambda: self.trier("poids"))
        layout_haut.addWidget(self.btn_trier_poids)

        layout.addLayout(layout_haut)

        self.tableau = QTableWidget()
        self.tableau.setColumnCount(7)
        self.tableau.setHorizontalHeaderLabels(
            ["ID", "Nom", "Espece", "Age (ans)", "Poids (kg)", "Enclos", "Sante"]
        )
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableau.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.tableau)

        layout_bas = QHBoxLayout()

        self.btn_ajouter = QPushButton("Ajouter un animal")
        self.btn_ajouter.clicked.connect(self.ajouter_animal)
        layout_bas.addWidget(self.btn_ajouter)

        self.btn_modifier = QPushButton("Modifier l'animal")
        self.btn_modifier.clicked.connect(self.modifier_animal)
        layout_bas.addWidget(self.btn_modifier)

        self.btn_supprimer = QPushButton("Supprimer l'animal")
        self.btn_supprimer.clicked.connect(self.supprimer_animal)
        layout_bas.addWidget(self.btn_supprimer)

        layout.addLayout(layout_bas)

    def init_tab_stats(self):
        layout = QVBoxLayout(self.tab_stats)

        self.zone_stats = QTextEdit()
        self.zone_stats.setReadOnly(True)
        layout.addWidget(self.zone_stats)

        self.btn_actualiser_stats = QPushButton("Actualiser les statistiques")
        self.btn_actualiser_stats.clicked.connect(self.afficher_statistiques)
        layout.addWidget(self.btn_actualiser_stats)

    def rafraichir_tableau(self, liste=None):
        if liste is None:
            liste = self.gestion.liste_animaux

        self.tableau.setRowCount(len(liste))
        for row, a in enumerate(liste):
            self.tableau.setItem(row, 0, QTableWidgetItem(str(a.identifiant)))
            self.tableau.setItem(row, 1, QTableWidgetItem(str(a.nom)))
            self.tableau.setItem(row, 2, QTableWidgetItem(str(a.espece)))
            self.tableau.setItem(row, 3, QTableWidgetItem(str(a.age)))
            self.tableau.setItem(row, 4, QTableWidgetItem(str(a.poids)))
            self.tableau.setItem(row, 5, QTableWidgetItem(str(a.enclos)))
            self.tableau.setItem(row, 6, QTableWidgetItem(str(a.statut_sante)))

        self.afficher_statistiques()

    def ajouter_animal(self):
        dialog = AnimalDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                nouveau = Animal(**data)
                self.gestion.ajouter_animal(nouveau)
                self.rafraichir_tableau()
                QMessageBox.information(self, "Succes", "Animal ajoute avec succes !")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))

    def modifier_animal(self):
        ligne_selectionnee = self.tableau.currentRow()
        if ligne_selectionnee < 0:
            QMessageBox.warning(self, "Attention", "Veuillez selectionner un animal a modifier.")
            return

        identifiant = self.tableau.item(ligne_selectionnee, 0).text()
        animal_cible = None
        for a in self.gestion.liste_animaux:
            if str(a.identifiant) == identifiant:
                animal_cible = a
                break

        if animal_cible:
            dialog = AnimalDialog(self, animal=animal_cible)
            if dialog.exec():
                data = dialog.get_data()
                try:
                    self.gestion.modifier_animal(
                        identifiant,
                        nom=data["nom"],
                        espece=data["espece"],
                        age=data["age"],
                        poids=data["poids"],
                        enclos=data["enclos"],
                        statut_sante=data["statut_sante"]
                    )
                    self.rafraichir_tableau()
                    QMessageBox.information(self, "Succes", "Animal modifie avec succes !")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", str(e))

    def supprimer_animal(self):
        ligne_selectionnee = self.tableau.currentRow()
        if ligne_selectionnee < 0:
            QMessageBox.warning(self, "Attention", "Veuillez selectionner un animal a supprimer.")
            return

        identifiant = self.tableau.item(ligne_selectionnee, 0).text()

        confirmation = QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous vraiment supprimer l'animal ID {identifiant} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            self.gestion.supprimer_animal(identifiant)
            self.rafraichir_tableau()
            QMessageBox.information(self, "Succes", "Animal supprime.")

    def rechercher_animaux(self, texte):
        resultats = self.gestion.rechercher_animal(texte)
        self.rafraichir_tableau(resultats)

    def trier(self, critere):
        liste_triee = self.gestion.classer_animaux(critere=critere)
        self.rafraichir_tableau(liste_triee)

    def afficher_statistiques(self):
        stats = self.gestion.afficher_statistiques()
        if not stats:
            self.zone_stats.setText("Aucune donnee disponible dans le zoo.")
            return

        doyen = self.gestion.doyen()
        plus_lourd = self.gestion.plus_lourd()

        texte = "=== STATISTIQUES GENERALES DU ZOO ===\n\n"
        texte += f"- Nombre total d'animaux : {stats['total']}\n"
        texte += f"- Age moyen : {stats['age_moyen']} ans (Min: {stats['age_min']}, Max: {stats['age_max']})\n"
        texte += f"- Poids moyen : {stats['poids_moyen']} kg (Min: {stats['poids_min']}, Max: {stats['poids_max']})\n\n"

        if doyen:
            texte += f"Doyen du zoo : {doyen.nom} ({doyen.espece}), {doyen.age} ans\n"
        if plus_lourd:
            texte += f"Animal le plus lourd : {plus_lourd.nom} ({plus_lourd.espece}), {plus_lourd.poids} kg\n\n"

        texte += "--- Repartition par Sante ---\n"
        for statut, count in stats['stats_sante'].items():
            texte += f"  - {statut} : {count}\n"

        texte += "\n--- Repartition par Espece ---\n"
        for esp, count in stats['stats_espece'].items():
            texte += f"  - {esp} : {count}\n"

        self.zone_stats.setText(texte)

    # ==========================================
    # MENU FICHIER : IMPORTER / EXPORTER / ENREGISTRER
    # ==========================================

    def creer_menu(self):
        menu_fichier = self.menuBar().addMenu("Fichier")

        action_importer = menu_fichier.addAction("Importer CSV")
        action_importer.triggered.connect(self.importer_csv)

        action_exporter = menu_fichier.addAction("Exporter CSV")
        action_exporter.triggered.connect(self.exporter_csv)

        menu_fichier.addSeparator()

        action_enregistrer = menu_fichier.addAction("Enregistrer")
        action_enregistrer.setShortcut("Ctrl+S")
        action_enregistrer.triggered.connect(self.enregistrer)

    def actualiser_tout(self):
        """Vide la recherche, puis rafraichit le tableau ET les statistiques."""
        self.input_recherche.blockSignals(True)
        self.input_recherche.clear()
        self.input_recherche.blockSignals(False)
        self.rafraichir_tableau()

    def importer_csv(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Importer un fichier CSV", "", "Fichiers CSV (*.csv)"
        )
        if not chemin:
            return
        try:
            nombre = self.gestion.importer_csv(chemin)
            self.actualiser_tout()
            QMessageBox.information(self, "Succes", f"{nombre} animal(aux) importe(s).")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Echec de l'importation : {e}")

    def exporter_csv(self):
        chemin, _ = QFileDialog.getSaveFileName(
            self, "Exporter en CSV", "export_animaux.csv", "Fichiers CSV (*.csv)"
        )
        if not chemin:
            return
        try:
            nombre = self.gestion.exporter_csv(chemin)
            QMessageBox.information(self, "Succes", f"{nombre} animal(aux) exporte(s).")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Echec de l'exportation : {e}")

    def enregistrer(self):
        try:
            self.gestion.enregistrer()
            self.actualiser_tout()
            QMessageBox.information(self, "Succes", "Modifications enregistrees !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Echec de l'enregistrement : {e}")