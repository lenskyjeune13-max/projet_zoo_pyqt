import csv
import os
from animal import Animal

EN_TETES_CSV = ["identifiant", "nom", "espece", "age", "poids", "enclos", "statut_sante"]


class GestionZoo:
    def __init__(self, chemin_fichier_csv="animaux.csv"):
        self.chemin_fichier_csv = chemin_fichier_csv
        self.liste_animaux = []
        self.charger_depuis_csv()

    def charger_depuis_csv(self):
        """Charge les animaux depuis le fichier CSV au démarrage."""
        self.liste_animaux = []
        if not os.path.exists(self.chemin_fichier_csv):
            # Si le fichier n'existe pas, on le crée avec les en-têtes
            self.sauvegarder_dans_csv()
            return

        try:
            with open(self.chemin_fichier_csv, mode="r", encoding="utf-8") as fichier:
                lecteur = csv.DictReader(fichier)
                for ligne in lecteur:
                    try:
                        animal = Animal(
                            identifiant=ligne["identifiant"],
                            nom=ligne["nom"],
                            espece=ligne["espece"],
                            age=ligne["age"],
                            poids=ligne["poids"],
                            enclos=ligne["enclos"],
                            statut_sante=ligne["statut_sante"]
                        )
                        self.liste_animaux.append(animal)
                    except Exception:
                        # Ignore les lignes mal formées pour ne pas faire planter l'app
                        continue
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier CSV : {e}")

    def sauvegarder_dans_csv(self, chemin=None):
        """Sauvegarde la liste actuelle des animaux dans un fichier CSV.
        Sans argument : fichier principal. Avec 'chemin' : fichier choisi (export)."""
        destination = chemin or self.chemin_fichier_csv
        try:
            with open(destination, mode="w", newline="", encoding="utf-8") as fichier:
                writer = csv.DictWriter(fichier, fieldnames=EN_TETES_CSV)
                writer.writeheader()
                for animal in self.liste_animaux:
                    writer.writerow(animal.to_dict())
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde dans le fichier CSV : {e}")

    def ajouter_animal(self, animal):
        """Ajoute un animal après avoir vérifié que l'identifiant est unique."""
        for a in self.liste_animaux:
            if a.identifiant == animal.identifiant:
                raise ValueError(f"Un animal avec l'identifiant '{animal.identifiant}' existe déjà.")
        self.liste_animaux.append(animal)
        self.sauvegarder_dans_csv()

    def supprimer_animal(self, identifiant):
        """Supprime un animal par son identifiant."""
        for i, a in enumerate(self.liste_animaux):
            if a.identifiant == identifiant:
                del self.liste_animaux[i]
                self.sauvegarder_dans_csv()
                return True
        return False

    def modifier_animal(self, identifiant, **kwargs):
        """Modifie les informations d'un animal existant."""
        for a in self.liste_animaux:
            if a.identifiant == identifiant:
                a.modifier_infos(**kwargs)
                self.sauvegarder_dans_csv()
                return True
        raise ValueError("Animal introuvable.")

    def rechercher_animal(self, texte):
        """Recherche des animaux par nom, espèce ou identifiant."""
        texte = texte.lower().strip()
        resultats = []
        for a in self.liste_animaux:
            if (texte in a.nom.lower() or
                texte in a.espece.lower() or
                texte in a.identifiant.lower()):
                resultats.append(a)
        return resultats

    def doyen(self):
        """Retourne l'animal le plus âgé en utilisant max()."""
        if not self.liste_animaux:
            return None
        return max(self.liste_animaux, key=lambda a: a.age)

    def plus_lourd(self):
        """Retourne l'animal le plus lourd en utilisant max()."""
        if not self.liste_animaux:
            return None
        return max(self.liste_animaux, key=lambda a: a.poids)

    def classer_animaux(self, critere="age", inverser=False):
        """Classe les animaux par âge ou poids en utilisant sorted()."""
        if critere == "age":
            return sorted(self.liste_animaux, key=lambda a: a.age, reverse=inverser)
        elif critere == "poids":
            return sorted(self.liste_animaux, key=lambda a: a.poids, reverse=inverser)
        return self.liste_animaux

    def afficher_statistiques(self):
        """Calcule et retourne les statistiques du zoo."""
        total = len(self.liste_animaux)
        if total == 0:
            return None

        ages = [a.age for a in self.liste_animaux]
        poids = [a.poids for a in self.liste_animaux]

        age_moyen = sum(ages) / total
        poids_moyen = sum(poids) / total

        stats_sante = {"Bon": 0, "Sous surveillance": 0, "Malade": 0}
        stats_espece = {}

        for a in self.liste_animaux:
            if a.statut_sante in stats_sante:
                stats_sante[a.statut_sante] += 1

            if a.espece in stats_espece:
                stats_espece[a.espece] += 1
            else:
                stats_espece[a.espece] = 1

        return {
            "total": total,
            "age_moyen": round(age_moyen, 2),
            "poids_moyen": round(poids_moyen, 2),
            "age_max": max(ages),
            "age_min": min(ages),
            "poids_max": max(poids),
            "poids_min": min(poids),
            "stats_sante": stats_sante,
            "stats_espece": stats_espece
        }

    # ==========================================
    # IMPORT / EXPORT / ENREGISTREMENT
    # ==========================================

    def importer_csv(self, chemin_source):
        """Lit un fichier CSV et AJOUTE les animaux dont l'identifiant n'existe pas encore.
        Les doublons et les lignes mal formées sont ignorés.
        Retourne le nombre d'animaux ajoutés. Lève une exception si le fichier est invalide."""
        ids_existants = {str(a.identifiant) for a in self.liste_animaux}
        ajoutes = 0

        with open(chemin_source, mode="r", newline="", encoding="utf-8") as fichier:
            lecteur = csv.DictReader(fichier)

            colonnes = set(lecteur.fieldnames or [])
            manquantes = [c for c in EN_TETES_CSV if c not in colonnes]
            if manquantes:
                raise ValueError("Colonnes manquantes dans le fichier : " + ", ".join(manquantes))

            for ligne in lecteur:
                try:
                    if str(ligne["identifiant"]) in ids_existants:
                        continue  # doublon : on ignore
                    animal = Animal(
                        identifiant=ligne["identifiant"],
                        nom=ligne["nom"],
                        espece=ligne["espece"],
                        age=ligne["age"],
                        poids=ligne["poids"],
                        enclos=ligne["enclos"],
                        statut_sante=ligne["statut_sante"]
                    )
                except Exception:
                    continue  # ligne mal formée : on ignore
                self.liste_animaux.append(animal)
                ids_existants.add(str(animal.identifiant))
                ajoutes += 1

        if ajoutes:
            self.sauvegarder_dans_csv()
        return ajoutes

    def exporter_csv(self, chemin_destination):
        """Écrit tous les animaux dans le fichier choisi. Retourne le nombre exporté."""
        self.sauvegarder_dans_csv(chemin_destination)
        return len(self.liste_animaux)

    def enregistrer(self):
        """Force la sauvegarde dans le fichier principal."""
        self.sauvegarder_dans_csv()
        return True