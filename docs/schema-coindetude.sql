-- ============================================================
-- CoinDetude — Schéma de base de données (PostgreSQL)
-- Organisé par module. MVP = phase 1, V2 = marqué explicitement.
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto; -- nécessaire pour gen_random_uuid()

-- ============================================================
-- 1. RÉFÉRENTIEL PÉDAGOGIQUE
-- ============================================================

CREATE TABLE niveaux (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nom TEXT NOT NULL UNIQUE,           -- '6ème', '5ème', ..., 'Terminale D'
  cycle TEXT NOT NULL CHECK (cycle IN ('college','lycee')),
  ordre INT NOT NULL                  -- pour trier l'affichage
);

CREATE TABLE matieres (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nom TEXT NOT NULL UNIQUE            -- 'Mathématiques', 'SVT', ...
);

CREATE TABLE niveaux_matieres (       -- quelles matières existent à quel niveau
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  niveau_id UUID NOT NULL REFERENCES niveaux(id) ON DELETE CASCADE,
  matiere_id UUID NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
  UNIQUE (niveau_id, matiere_id)
);

CREATE TABLE chapitres (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  matiere_id UUID NOT NULL REFERENCES matieres(id) ON DELETE CASCADE,
  niveau_id UUID NOT NULL REFERENCES niveaux(id) ON DELETE CASCADE,
  titre TEXT NOT NULL,
  ordre INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 2. UTILISATEURS & AUTHENTIFICATION
-- ============================================================

CREATE TABLE utilisateurs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role TEXT NOT NULL CHECK (role IN ('eleve','parent','enseignant','admin')),
  nom_complet TEXT NOT NULL,
  telephone TEXT NOT NULL UNIQUE,
  email TEXT UNIQUE,
  mot_de_passe_hash TEXT NOT NULL,
  niveau_id UUID REFERENCES niveaux(id),   -- renseigné uniquement si role = 'eleve'
  photo_url TEXT,
  statut TEXT NOT NULL DEFAULT 'actif' CHECK (statut IN ('actif','suspendu','supprime')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  token_hash TEXT NOT NULL,
  expire_at TIMESTAMPTZ NOT NULL,
  revoque BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE liaisons_parent (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  eleve_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  code_invitation TEXT UNIQUE,
  statut TEXT NOT NULL DEFAULT 'actif' CHECK (statut IN ('en_attente','actif','revoque')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (parent_id, eleve_id)
);

-- ============================================================
-- 3. CONTENU PÉDAGOGIQUE
-- ============================================================

CREATE TABLE ressources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chapitre_id UUID REFERENCES chapitres(id) ON DELETE SET NULL, -- NULL pour une annale non rattachée à un chapitre précis
  type TEXT NOT NULL CHECK (type IN ('cours','exercice','corrige','annale')),
  titre TEXT NOT NULL,
  contenu_texte TEXT,                 -- pour un résumé de cours généré/relu
  fichier_path TEXT,                  -- chemin objet storage (PDF scanné, etc.)
  annee_session INT,                  -- pertinent pour type = 'annale'
  source_url TEXT,
  contenu_hash TEXT UNIQUE,           -- déduplication
  origine TEXT NOT NULL DEFAULT 'scraper' CHECK (origine IN ('scraper','ia','enseignant','admin')),
  cree_par_utilisateur_id UUID REFERENCES utilisateurs(id),  -- renseigné si origine = 'enseignant' ou 'admin'
  statut TEXT NOT NULL DEFAULT 'a_valider' CHECK (statut IN ('a_valider','valide','rejete')),
  valide_par_id UUID REFERENCES utilisateurs(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE progression_eleve (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  chapitre_id UUID NOT NULL REFERENCES chapitres(id) ON DELETE CASCADE,
  statut TEXT NOT NULL DEFAULT 'non_commence' CHECK (statut IN ('non_commence','en_cours','termine')),
  derniere_consultation TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (utilisateur_id, chapitre_id)
);

-- ============================================================
-- 4. ASSISTANT IA
-- ============================================================

CREATE TABLE conversations_ia (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  chapitre_id UUID REFERENCES chapitres(id),
  titre TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE messages_ia (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations_ia(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('utilisateur','assistant')),
  contenu TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- V2
CREATE TABLE corrections_dissertation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  matiere_id UUID NOT NULL REFERENCES matieres(id),
  texte_soumis TEXT NOT NULL,
  feedback TEXT,
  note_estimee NUMERIC(4,2),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 5. CALENDRIER, ACTUALITÉS ET RÉSULTATS
-- ============================================================

CREATE TABLE evenements_calendrier (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  titre TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('rentree','examen','composition','conge','concours','resultat')),
  niveau_id UUID REFERENCES niveaux(id),   -- NULL = concerne tous les niveaux
  date_debut DATE NOT NULL,
  date_fin DATE,
  statut_fiabilite TEXT NOT NULL DEFAULT 'a_valider' CHECK (statut_fiabilite IN ('a_valider','confirme')),
  source TEXT,
  cree_par TEXT NOT NULL DEFAULT 'admin' CHECK (cree_par IN ('admin','scraper')),
  valide_par_id UUID REFERENCES utilisateurs(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE actualites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  titre TEXT NOT NULL,
  resume TEXT NOT NULL,               -- reformulation originale, jamais copiée d'une source
  lien_source TEXT NOT NULL,
  categorie TEXT NOT NULL CHECK (categorie IN ('officiel','concours','vie_scolaire')),
  date_publication TIMESTAMPTZ NOT NULL DEFAULT now(),
  evenement_lie_id UUID REFERENCES evenements_calendrier(id)
);

CREATE TABLE profils_examen (
  utilisateur_id UUID PRIMARY KEY REFERENCES utilisateurs(id) ON DELETE CASCADE,
  numero_table TEXT,
  examen_suivi TEXT CHECK (examen_suivi IN ('CEPD','BEPC','BAC1','BAC2')),
  session_annee INT
);

CREATE TABLE abonnements_rappel (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  evenement_id UUID NOT NULL REFERENCES evenements_calendrier(id) ON DELETE CASCADE,
  delai TEXT NOT NULL CHECK (delai IN ('j7','j1','jour_j')),
  envoye BOOLEAN NOT NULL DEFAULT false,
  UNIQUE (utilisateur_id, evenement_id, delai)
);

CREATE TABLE device_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  token_fcm TEXT NOT NULL UNIQUE,
  plateforme TEXT NOT NULL CHECK (plateforme IN ('android','ios')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE notifications_envoyees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  titre TEXT NOT NULL,
  corps TEXT NOT NULL,
  type TEXT NOT NULL,                 -- 'rappel_calendrier' | 'resultat_disponible' | 'actualite'
  envoye_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  lu BOOLEAN NOT NULL DEFAULT false
);

-- ============================================================
-- 6. PAIEMENT ET ABONNEMENT
-- ============================================================

CREATE TABLE abonnements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('matiere','niveau_complet')),
  matiere_id UUID REFERENCES matieres(id),   -- renseigné si type = 'matiere'
  niveau_id UUID REFERENCES niveaux(id),     -- renseigné si type = 'niveau_complet'
  statut TEXT NOT NULL DEFAULT 'actif' CHECK (statut IN ('actif','expire','annule')),
  date_debut TIMESTAMPTZ NOT NULL DEFAULT now(),
  date_fin TIMESTAMPTZ
);

-- fournisseur : agrégateur de paiement mobile money togolais (ex. PayGate Global, CinetPay)
CREATE TABLE transactions_paiement (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  abonnement_id UUID REFERENCES abonnements(id),
  montant NUMERIC(10,2) NOT NULL,
  devise TEXT NOT NULL DEFAULT 'XOF',
  moyen_paiement TEXT NOT NULL CHECK (moyen_paiement IN ('tmoney','flooz')),
  fournisseur TEXT NOT NULL,          -- 'paygate' | 'cinetpay' | ...
  reference_externe TEXT,             -- id de transaction côté fournisseur
  statut TEXT NOT NULL DEFAULT 'en_attente' CHECK (statut IN ('en_attente','confirme','echoue')),
  callback_recu_at TIMESTAMPTZ,       -- horodatage de la confirmation webhook
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 7. MARKETPLACE ENSEIGNANTS — V2
-- ============================================================

CREATE TABLE enseignants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL UNIQUE REFERENCES utilisateurs(id) ON DELETE CASCADE,
  bio TEXT,
  statut_verification TEXT NOT NULL DEFAULT 'en_attente' CHECK (statut_verification IN ('en_attente','verifie','rejete')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE offres_enseignant (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enseignant_id UUID NOT NULL REFERENCES enseignants(id) ON DELETE CASCADE,
  titre TEXT NOT NULL,
  description TEXT,
  prix NUMERIC(10,2) NOT NULL,
  matiere_id UUID REFERENCES matieres(id),
  niveau_id UUID REFERENCES niveaux(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE abonnements_offre (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  offre_id UUID NOT NULL REFERENCES offres_enseignant(id) ON DELETE CASCADE,
  statut TEXT NOT NULL DEFAULT 'actif' CHECK (statut IN ('actif','expire','annule')),
  date_debut TIMESTAMPTZ NOT NULL DEFAULT now(),
  date_fin TIMESTAMPTZ
);

-- ============================================================
-- 8. GAMIFICATION — V2
-- ============================================================

CREATE TABLE defis (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chapitre_id UUID NOT NULL REFERENCES chapitres(id) ON DELETE CASCADE,
  titre TEXT NOT NULL,
  duree_secondes INT NOT NULL,
  questions_json JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE resultats_defi (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_id UUID NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
  defi_id UUID NOT NULL REFERENCES defis(id) ON DELETE CASCADE,
  score INT NOT NULL,
  temps_ecoule_secondes INT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- 9. ADMINISTRATION
-- ============================================================

CREATE TABLE logs_moderation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  utilisateur_admin_id UUID NOT NULL REFERENCES utilisateurs(id),
  cible_type TEXT NOT NULL,           -- 'ressource' | 'evenement_calendrier' | 'enseignant' | ...
  cible_id UUID,
  action TEXT NOT NULL,               -- 'valide' | 'rejete' | 'suspendu' | ...
  commentaire TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- INDEX RECOMMANDÉS
-- ============================================================

CREATE INDEX idx_chapitres_matiere_niveau ON chapitres(matiere_id, niveau_id);
CREATE INDEX idx_ressources_chapitre ON ressources(chapitre_id);
CREATE INDEX idx_ressources_statut ON ressources(statut);
CREATE INDEX idx_progression_utilisateur ON progression_eleve(utilisateur_id);
CREATE INDEX idx_messages_ia_conversation ON messages_ia(conversation_id);
CREATE INDEX idx_evenements_date ON evenements_calendrier(date_debut);
CREATE INDEX idx_transactions_utilisateur ON transactions_paiement(utilisateur_id);
CREATE INDEX idx_notifications_utilisateur ON notifications_envoyees(utilisateur_id);
CREATE INDEX idx_offres_matiere_niveau ON offres_enseignant(matiere_id, niveau_id);
