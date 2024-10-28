#!/bin/bash

#Ce script doit créer des nouveaux Utilisateur

#vérification d'argument
if [ $# -eq 0 ];
then
		echo "Il manque les noms d'utilisateurs en argument"
	exit 1
fi

#Vérification si le nom existe déjà si non création de(s)l'Utilisateur(s)

for passwd in "$@";
do
	if cat /etc/passwd | grep -q $passwd
	then
		echo "Le nom d'utilisateur '$passwd' existe déjà"
	else
			useradd $passwd
			if [ $? -eq 0 ];
			then
				echo "l'utilisateur '$passwd' a été crée."
			else
				echo "Erreur à la création de l'utilisateur '$passwd'"
			fi
	fi
done