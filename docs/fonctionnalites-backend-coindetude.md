# Fonctionnalités backend — CoinDetude

Ce document liste ce que l'API doit exposer, module par module, en s'appuyant sur `schema-coindetude.sql`. Les endpoints indiqués sont des esquisses (méthode + chemin) pour cadrer le développement FastAPI, pas une spec figée.

**MVP** = à construire en priorité. **V2** = prévu, pas prioritaire.

---

## 1. Authentification et comptes (MVP)

- Inscription élève ou parent — `POST /auth/register`
- Connexion — `POST /auth/login`
- Rafraîchissement du token d'accès — `POST /auth/refresh`
- Déconnexion (révocation du refresh token) — `POST /auth/logout`
- Consultation du profil courant — `GET /users/me`
- Mise à jour du profil — `PATCH /users/me`
- Génération d'un code d'invitation parent par l'élève — `POST /users/me/invite-parent`
- Liaison d'un compte parent à un élève via le code — `POST /parent/link`
- Révocation d'une liaison parent-élève — `DELETE /parent/link/{id}`

## 2. Référentiel pédagogique et contenu (MVP)

- Liste des niveaux scolaires — `GET /niveaux`
- Liste des matières disponibles pour un niveau — `GET /niveaux/{id}/matieres`
- Liste des chapitres d'une matière pour un niveau — `GET /chapitres?matiere_id=&niveau_id=`
- Détail d'un chapitre avec ses ressources (cours, exercices, corrigés, annales) — `GET /chapitres/{id}`
- Recherche de contenu (mot-clé) — `GET /ressources/recherche?q=`
- Téléchargement d'une ressource pour le mode hors-ligne — `GET /ressources/{id}/telecharger`
- Marquage de la progression d'un chapitre (en cours / terminé) — `POST /chapitres/{id}/progression`
- Consultation de la progression globale de l'élève — `GET /users/me/progression`

**Back-office (admin) :**
- File d'attente du contenu scrapé à valider — `GET /admin/ressources?statut=a_valider`
- Validation ou rejet d'une ressource — `POST /admin/ressources/{id}/valider`
- Création manuelle d'une ressource (contenu généré/rédigé par l'équipe) — `POST /admin/ressources`

## 3. Assistant IA (MVP partiel)

- Démarrer une conversation de révision ancrée sur un chapitre — `POST /ia/conversations`
- Envoyer un message dans une conversation — `POST /ia/conversations/{id}/messages`
- Historique d'une conversation — `GET /ia/conversations/{id}`
- Générer des exercices personnalisés selon les lacunes détectées — `POST /ia/exercices/generer`
- **V2** — Corriger une dissertation/rédaction — `POST /ia/corrections`
- **V2** — Simulation d'oral — `POST /ia/oral/simuler`

## 4. Calendrier, actualités et résultats (MVP)

- Liste des événements du calendrier, filtrable par niveau — `GET /calendrier?niveau_id=`
- Détail d'un événement — `GET /calendrier/{id}`
- S'abonner à un rappel sur un événement (J-7, J-1, jour J) — `POST /calendrier/{id}/rappel`
- Se désabonner d'un rappel — `DELETE /calendrier/{id}/rappel`
- Fil d'actualités scolaires — `GET /actualites`
- Enregistrer/mettre à jour son numéro de table — `POST /users/me/profil-examen`
- Rechercher un résultat d'examen — `GET /resultats?nom=&numero_table=&examen=` (redirection encadrée vers la plateforme officielle en MVP, voir cahier des charges du module)
- Tâche planifiée : détection et envoi des rappels dus (job interne, pas un endpoint utilisateur)

**Back-office (admin) :**
- File de validation des événements détectés par scraping — `GET /admin/calendrier?statut=a_valider`
- Validation ou correction d'un événement avant publication — `POST /admin/calendrier/{id}/valider`
- Publication d'une actualité — `POST /admin/actualites`

## 5. Paiement et abonnement (MVP)

- Lister les offres d'abonnement disponibles — `GET /abonnements/offres`
- Initier un paiement mobile money (T-Money ou Flooz) — `POST /paiements/initier`
- Callback de confirmation du fournisseur de paiement (webhook) — `POST /paiements/callback`
- Statut de l'abonnement actif de l'utilisateur — `GET /users/me/abonnement`
- Historique des transactions — `GET /users/me/transactions`

> Point technique à trancher avant l'implémentation : le fournisseur de paiement. PayGate Global est togolais, gère spécifiquement T-Money et Flooz, et propose un compte et un accès API gratuits — un bon point de départ pour le MVP. CinetPay couvre plusieurs pays d'Afrique de l'Ouest et peut avoir du sens si tu envisages une expansion régionale plus tôt que prévu. Dans les deux cas, la confirmation de paiement est asynchrone (webhook/callback), d'où le champ `callback_recu_at` dans le schéma — l'abonnement ne doit s'activer qu'à réception de cette confirmation, jamais juste après l'initiation du paiement.

## 6. Espace parent (MVP léger)

- Vue de la progression de l'enfant lié — `GET /parent/enfants/{id}/progression`
- Vue du calendrier de l'enfant lié — `GET /parent/enfants/{id}/calendrier`
- Vue du dernier résultat consulté par l'enfant lié — `GET /parent/enfants/{id}/resultat`

## 7. Notifications (MVP)

- Enregistrement d'un token FCM (à l'ouverture de l'app) — `POST /notifications/device-token`
- Historique des notifications reçues — `GET /users/me/notifications`
- Marquer une notification comme lue — `PATCH /users/me/notifications/{id}`
- Mise à jour des préférences de notification par catégorie — `PATCH /users/me/notifications/preferences`

## 8. Marketplace enseignants — V2

- Inscription en tant qu'enseignant — `POST /enseignants/register`
- Vérification du compte enseignant (admin) — `POST /admin/enseignants/{id}/verifier`
- Publication d'une offre de contenu — `POST /enseignants/offres`
- Modification/retrait d'une offre — `PATCH /enseignants/offres/{id}`
- Abonnement d'un élève à une offre enseignant — `POST /offres/{id}/abonner`
- Tableau de bord enseignant (revenus, abonnés) — `GET /enseignants/me/dashboard`

## 9. Gamification — V2

- Liste des défis disponibles pour un chapitre — `GET /chapitres/{id}/defis`
- Soumission d'un résultat de défi — `POST /defis/{id}/resultat`
- Classement (par niveau, par établissement si renseigné) — `GET /classement`

## 10. Administration et analyse (MVP)

- Tableau de bord (indicateurs clés : utilisateurs actifs, conversions, contenu en attente) — `GET /admin/dashboard`
- Journal des actions de modération — `GET /admin/logs`
- Export de rapports statistiques — `GET /admin/rapports?periode=`

---

## Notes transverses

- **Autorisation** : chaque endpoint doit vérifier le rôle de l'utilisateur (`eleve`, `parent`, `enseignant`, `admin`) avant d'exécuter l'action — particulièrement critique pour tout ce qui touche à l'espace parent (lecture seule stricte) et à la validation de contenu (admin uniquement).
- **Conformité données personnelles** : les endpoints touchant `profils_examen` et `resultats` manipulent des données personnelles d'élèves majoritairement mineurs — traitement à déclarer auprès de l'IPDCP conformément à la loi togolaise n°2019-014 (voir cahier des charges du module actualités).
- **Idempotence des paiements** : le endpoint de callback (`POST /paiements/callback`) doit être conçu pour être appelé plusieurs fois sans effet de bord (les fournisseurs mobile money peuvent renvoyer la même confirmation) — vérifier `reference_externe` avant de ré-activer un abonnement déjà actif.
