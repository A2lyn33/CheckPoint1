#!/usr/bin/env bash
# Exercice d'administration Linux : créer des comptes locaux sans mot de passe partagé.
set -u

usage() {
    printf 'Usage : bash %s [--dry-run] utilisateur [utilisateur ...]\n' "$0"
}

dry_run=false
case "${1:-}" in
    --help|-h) usage; exit 0 ;;
    --dry-run) dry_run=true; shift ;;
esac

if (( $# == 0 )); then
    usage >&2
    exit 2
fi

# Valider tout le lot avant une première création.
for username in "$@"; do
    if [[ ! "$username" =~ ^[a-z_][a-z0-9_-]{0,31}$ ]]; then
        printf 'Nom invalide : %s (1 à 32 caractères : minuscules, chiffres, _ et -).\n' "$username" >&2
        exit 2
    fi
done

if [[ "$dry_run" == false ]] && (( EUID != 0 )); then
    printf 'La création nécessite les droits root. Utiliser sudo ou --dry-run.\n' >&2
    exit 1
fi

if ! command -v getent >/dev/null 2>&1; then
    printf 'Commande manquante : getent.\n' >&2
    exit 1
fi
if [[ "$dry_run" == false ]] && ! command -v useradd >/dev/null 2>&1; then
    printf 'Commande manquante : useradd.\n' >&2
    exit 1
fi

status=0
for username in "$@"; do
    # Recherche exacte via NSS : évite de confondre alice avec alice2.
    if getent passwd "$username" >/dev/null; then
        printf 'Déjà présent : %s\n' "$username"
        continue
    else
        lookup_status=$?
        if (( lookup_status != 2 )); then
            printf 'Échec de consultation des comptes pour %s (code %s).\n' "$username" "$lookup_status" >&2
            status=1
            continue
        fi
    fi

    if [[ "$dry_run" == true ]]; then
        printf 'Simulation : création de %s avec dossier personnel et shell Bash.\n' "$username"
    elif useradd --create-home --shell /bin/bash -- "$username"; then
        printf 'Compte créé : %s. Aucun mot de passe défini par ce script.\n' "$username"
    else
        printf 'Échec de création : %s\n' "$username" >&2
        status=1
    fi
done
exit "$status"
