# Administration Linux — comptes utilisateurs et exercices système
**Exercice de formation · Bash · version relue en novembre 2026**

## Créer des comptes locaux

[addUsers.sh](addUsers.sh) traite les noms fournis en argument, repère les comptes existants et crée les comptes manquants avec un dossier personnel et un shell Bash.

### Utilisation

```bash
# Vérifier les actions prévues sans créer de compte
bash addUsers.sh --dry-run alice bob

# Dans une VM de laboratoire, après lecture de la simulation
sudo bash addUsers.sh alice bob
```

Aucun mot de passe n'est inscrit dans le script. La commande ne définit pas de mot de passe : le mode d'accès devra être configuré séparément selon les règles du laboratoire.

### Améliorations apportées

- Recherche exacte avec `getent passwd` à la place d'une recherche partielle dans `/etc/passwd`.
- Validation de tous les noms avant le début des créations.
- Arguments correctement protégés ; noms simples de 1 à 32 caractères.
- Vérification des privilèges et des commandes nécessaires.
- Mode `--dry-run`, aide et code de retour non nul en cas d'échec.
- Fin de ligne Linux pour exécuter le fichier sous Bash.

**Limite :** un échec de création en cours de lot ne supprime pas les comptes déjà créés. Le script affiche l'erreur et termine avec le code 1. Le mode simulation ne vérifie pas toutes les contraintes de création de la machine.

## Vérification automatisée

```bash
bash -n addUsers.sh
python3 -m unittest discover -s tests -v
```

Les tests remplacent `getent` et `useradd` par des commandes simulées : **aucun compte réel n'est créé**.

Vérification du 2 novembre 2026 : syntaxe Bash valide ; huit tests réussis ; le test de refus pour un utilisateur non privilégié a été ignoré, car l'environnement de vérification ne permettait pas de changer d'UID. La création réelle de comptes reste à vérifier dans une VM jetable.

Cette révision et les tests ont été préparés avec une assistance IA à partir du script de formation initial.

## Autres travaux du checkpoint

- [Exercice 1 et captures](Exercice1.md)
- [Exercice 3](Exercice%203.md)

## Références

[Debian — getent](https://manpages.debian.org/bookworm/manpages/getent.1.en.html) · [Debian — useradd](https://manpages.debian.org/bookworm/passwd/useradd.8.en.html)

[Retour au portfolio](https://github.com/A2lyn33)
