class Animal:
    def __init__(self, identifiant, nom, espece, age, poids, enclos, statut_sante):
        """Initialise un animal en validant toutes les contraintes métier."""
        if not str(identifiant).strip():
            raise ValueError("L'identifiant ne peut pas être vide.")
        if not nom or not nom.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        if not espece or not espece.strip():
            raise ValueError("L'espèce ne peut pas être vide.")
        
        try:
            age_int = int(age)
        except ValueError:
            raise ValueError("L'âge doit être un nombre entier.")
        if not (0 <= age_int <= 100):
            raise ValueError("L'âge doit être compris entre 0 et 100 ans.")

        try:
            poids_float = float(poids)
        except ValueError:
            raise ValueError("Le poids doit être un nombre.")
        if poids_float <= 0:
            raise ValueError("Le poids doit être strictement supérieur à 0.")

        if not enclos or not enclos.strip():
            raise ValueError("L'enclos doit obligatoirement être renseigné.")

        statuts_autorises = ["Bon", "Sous surveillance", "Malade"]
        if statut_sante not in statuts_autorises:
            raise ValueError(f"Le statut de santé doit être l'un des suivants : {', '.join(statuts_autorises)}.")

        self.identifiant = str(identifiant).strip()
        self.nom = nom.strip()
        self.espece = espece.strip()
        self.age = age_int
        self.poids = poids_float
        self.enclos = enclos.strip()
        self.statut_sante = statut_sante

    def modifier_infos(self, nom=None, espece=None, age=None, poids=None, enclos=None, statut_sante=None):
        """Modifie les informations de l'animal avec validation."""
        if nom is not None:
            if not nom.strip():
                raise ValueError("Le nom ne peut pas être vide.")
            self.nom = nom.strip()
        
        if espece is not None:
            if not espece.strip():
                raise ValueError("L'espèce ne peut pas être vide.")
            self.espece = espece.strip()

        if age is not None:
            try:
                age_int = int(age)
            except ValueError:
                raise ValueError("L'âge doit être un nombre entier.")
            if not (0 <= age_int <= 100):
                raise ValueError("L'âge doit être compris entre 0 et 100 ans.")
            self.age = age_int

        if poids is not None:
            try:
                poids_float = float(poids)
            except ValueError:
                raise ValueError("Le poids doit être un nombre.")
            if poids_float <= 0:
                raise ValueError("Le poids doit être strictement supérieur à 0.")
            self.poids = poids_float

        if enclos is not None:
            if not enclos.strip():
                raise ValueError("L'enclos doit obligatoirement être renseigné.")
            self.enclos = enclos.strip()

        if statut_sante is not None:
            statuts_autorises = ["Bon", "Sous surveillance", "Malade"]
            if statut_sante not in statuts_autorises:
                raise ValueError(f"Le statut de santé doit être l'un des suivants : {', '.join(statuts_autorises)}.")
            self.statut_sante = statut_sante

    def est_senior(self):
        """Détermine si l'animal est un senior (seuil fixé à 15 ans ou plus)."""
        return self.age >= 15

    def afficher_infos(self):
        """Renvoie une chaîne formatée avec les détails de l'animal."""
        return f"ID: {self.identifiant} | Nom: {self.nom} | Espèce: {self.espece} | Âge: {self.age} ans | Poids: {self.poids} kg | Enclos: {self.enclos} | Santé: {self.statut_sante}"

    def to_dict(self):
        """Convertit l'objet en dictionnaire pour faciliter l'écriture dans le fichier CSV."""
        return {
            "identifiant": self.identifiant,
            "nom": self.nom,
            "espece": self.espece,
            "age": self.age,
            "poids": self.poids,
            "enclos": self.enclos,
            "statut_sante": self.statut_sante
        }