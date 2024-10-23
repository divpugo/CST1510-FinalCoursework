# Coffee Beans Vending Machine

## Introduction
This repository hosts the code for "Coffee Beans," a client/server software system designed for CST 1510 - Final Coursework. The system simulates a vending machine for hot and cold coffee beverages, handling client interactions and server-side data storage efficiently. It supports multiple clients simultaneously and maintains an up-to-date stock through an intuitive graphical user interface.

## Features
- **User Interface:** Launches with a welcoming message on the main page.
- **Product Selection:** Displays product details such as ID, price, and quantity. Includes a graphical representation of stock levels.
- **Order Management:** Allows users to add products to their cart, review the transaction summary, and modify orders before finalizing the payment.
- **Payment Options:** Supports transactions through cash or card, providing change calculations for cash payments.
- **Transaction Finalization:** Displays a virtual receipt with detailed order and payment information, followed by a thank you message.

## System Operations
1. **Start Up:** Opens the main page with a welcoming greeting.
2. **Choose Product:** Users can select products, view details, and choose quantities.
3. **Modify Cart:** Options to add more products, finish the purchase, or cancel the transaction.
4. **Checkout:** After selecting "Finish and Pay," users review their virtual receipt and proceed to payment.
5. **Payment Process:** Options to pay by cash or card. If by cash, the machine calculates and displays the change.
6. **Completion:** Post-payment, a thank you message appears and the system resets for the next user.

## Getting Started
To run the Coffee Beans Vending Machine system:
```bash
python client.py
python server.py
```
Ensure both client and server scripts are running simultaneously for full functionality.

## Technologies used
-**Python:** Main programming language used for both client and server-side development.
-**Tkinter:** For creating the graphical user interface.

---

# Distributeur Automatique Coffee Beans
## Introduction

Ce dépôt contient le code pour "Coffee Beans", un système logiciel client/serveur conçu pour le cours CST 1510. Le système simule un distributeur de boissons caféinées chaudes et froides, gérant les interactions clients et le stockage des données côté serveur de manière efficace. Il prend en charge plusieurs clients simultanément et maintient un stock à jour grâce à une interface graphique intuitive.

## Fonctionnalités

-**Interface Utilisateur :** Lance avec un message de bienvenue sur la page principale.
-**Sélection de Produits :** Affiche les détails des produits tels que l'ID, le prix, et la quantité. Inclut une représentation graphique des niveaux de stock.
-**Gestion des Commandes :** Permet aux utilisateurs d'ajouter des produits à leur panier, de revoir le résumé de la transaction, et de modifier les commandes avant de finaliser le paiement.
-**Options de Paiement :** Prend en charge les transactions par espèces ou carte, fournissant des calculs de monnaie pour les paiements en espèces.
-**Finalisation de la Transaction :** Affiche un reçu virtuel avec des informations détaillées sur la commande et le paiement, suivi d'un message de remerciement.

## Opérations Système

-**Démarrage :** Ouvre la page principale avec un accueil chaleureux.
-**Choix du Produit :** Les utilisateurs peuvent sélectionner des produits, voir les détails et choisir les quantités.
-**Modifier le Panier :** Options pour ajouter plus de produits, terminer l'achat, ou annuler la transaction.
-**Paiement :** Après avoir sélectionné "Terminer et Payer", les utilisateurs passent en revue leur reçu virtuel et procèdent au paiement.
-**Processus de Paiement :** Options de paiement par espèces ou carte. Si paiement en espèces, la machine calcule et affiche la monnaie.
-**Achèvement :** Après le paiement, un message de remerciement apparaît et le système se réinitialise pour le prochain utilisateur.

## Pour Commencer

Pour exécuter le système du distributeur automatique Coffee Beans :

```bash

python client.py
python server.py
```
Assurez-vous que les scripts client et serveur fonctionnent simultanément pour une fonctionnalité complète.

## Technologies Utilisées

-**Python :** Langage de programmation principal utilisé pour le développement côté client et serveur.
-**Tkinter :** Pour créer l'interface graphique.
