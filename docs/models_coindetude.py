"""
Modèles SQLAlchemy 2.0 pour CoinDetude.
Traduction directe de schema-coindetude.sql — mêmes noms de tables/colonnes,
mêmes contraintes. Les relations ORM sont ajoutées pour les clés étrangères
non ambiguës ; les colonnes avec plusieurs FK vers `utilisateurs` (ex.
Ressource.cree_par_utilisateur_id / valide_par_id) restent de simples
colonnes typées pour éviter toute ambiguïté de relation.

Nécessite : sqlalchemy>=2.0
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def uuid_pk() -> Mapped[uuid.UUID]:
    """Raccourci pour une clé primaire UUID générée côté base (gen_random_uuid())."""
    return mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )


def created_at_col() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


# ============================================================
# 1. RÉFÉRENTIEL PÉDAGOGIQUE
# ============================================================

class Niveau(Base):
    __tablename__ = "niveaux"
    __table_args__ = (CheckConstraint("cycle IN ('college','lycee')", name="ck_niveaux_cycle"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    nom: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    cycle: Mapped[str] = mapped_column(String, nullable=False)
    ordre: Mapped[int] = mapped_column(Integer, nullable=False)

    chapitres: Mapped[list["Chapitre"]] = relationship(back_populates="niveau")


class Matiere(Base):
    __tablename__ = "matieres"

    id: Mapped[uuid.UUID] = uuid_pk()
    nom: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    chapitres: Mapped[list["Chapitre"]] = relationship(back_populates="matiere")


class NiveauMatiere(Base):
    """Table d'association : quelles matières existent à quel niveau."""
    __tablename__ = "niveaux_matieres"
    __table_args__ = (UniqueConstraint("niveau_id", "matiere_id", name="uq_niveau_matiere"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    niveau_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id", ondelete="CASCADE"), nullable=False
    )
    matiere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matieres.id", ondelete="CASCADE"), nullable=False
    )


class Chapitre(Base):
    __tablename__ = "chapitres"

    id: Mapped[uuid.UUID] = uuid_pk()
    matiere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matieres.id", ondelete="CASCADE"), nullable=False
    )
    niveau_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id", ondelete="CASCADE"), nullable=False
    )
    titre: Mapped[str] = mapped_column(String, nullable=False)
    ordre: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = created_at_col()

    matiere: Mapped["Matiere"] = relationship(back_populates="chapitres")
    niveau: Mapped["Niveau"] = relationship(back_populates="chapitres")
    ressources: Mapped[list["Ressource"]] = relationship(back_populates="chapitre")


# ============================================================
# 2. UTILISATEURS & AUTHENTIFICATION
# ============================================================

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    __table_args__ = (
        CheckConstraint("role IN ('eleve','parent','enseignant','admin')", name="ck_utilisateurs_role"),
        CheckConstraint("statut IN ('actif','suspendu','supprime')", name="ck_utilisateurs_statut"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    role: Mapped[str] = mapped_column(String, nullable=False)
    nom_complet: Mapped[str] = mapped_column(String, nullable=False)
    telephone: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(String, nullable=False)
    niveau_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id")
    )  # renseigné uniquement si role = 'eleve'
    photo_url: Mapped[Optional[str]] = mapped_column(String)
    statut: Mapped[str] = mapped_column(String, nullable=False, default="actif")
    created_at: Mapped[datetime] = created_at_col()
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="utilisateur")
    progression: Mapped[list["ProgressionEleve"]] = relationship(back_populates="utilisateur")
    abonnements: Mapped[list["Abonnement"]] = relationship(back_populates="utilisateur")
    device_tokens: Mapped[list["DeviceToken"]] = relationship(back_populates="utilisateur")
    profil_examen: Mapped[Optional["ProfilExamen"]] = relationship(back_populates="utilisateur")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String, nullable=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoque: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = created_at_col()

    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="refresh_tokens")


class LiaisonParent(Base):
    __tablename__ = "liaisons_parent"
    __table_args__ = (
        CheckConstraint("statut IN ('en_attente','actif','revoque')", name="ck_liaison_statut"),
        UniqueConstraint("parent_id", "eleve_id", name="uq_parent_eleve"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    eleve_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    code_invitation: Mapped[Optional[str]] = mapped_column(String, unique=True)
    statut: Mapped[str] = mapped_column(String, nullable=False, default="actif")
    created_at: Mapped[datetime] = created_at_col()


# ============================================================
# 3. CONTENU PÉDAGOGIQUE
# ============================================================

class Ressource(Base):
    __tablename__ = "ressources"
    __table_args__ = (
        CheckConstraint("type IN ('cours','exercice','corrige','annale')", name="ck_ressources_type"),
        CheckConstraint(
            "origine IN ('scraper','ia','enseignant','admin')", name="ck_ressources_origine"
        ),
        CheckConstraint("statut IN ('a_valider','valide','rejete')", name="ck_ressources_statut"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    chapitre_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chapitres.id", ondelete="SET NULL")
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
    titre: Mapped[str] = mapped_column(String, nullable=False)
    contenu_texte: Mapped[Optional[str]] = mapped_column(Text)
    fichier_path: Mapped[Optional[str]] = mapped_column(String)
    annee_session: Mapped[Optional[int]] = mapped_column(Integer)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    contenu_hash: Mapped[Optional[str]] = mapped_column(String, unique=True)
    origine: Mapped[str] = mapped_column(String, nullable=False, default="scraper")
    cree_par_utilisateur_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id")
    )
    statut: Mapped[str] = mapped_column(String, nullable=False, default="a_valider")
    valide_par_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id")
    )
    created_at: Mapped[datetime] = created_at_col()

    chapitre: Mapped[Optional["Chapitre"]] = relationship(back_populates="ressources")


class ProgressionEleve(Base):
    __tablename__ = "progression_eleve"
    __table_args__ = (
        CheckConstraint(
            "statut IN ('non_commence','en_cours','termine')", name="ck_progression_statut"
        ),
        UniqueConstraint("utilisateur_id", "chapitre_id", name="uq_progression_utilisateur_chapitre"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    chapitre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chapitres.id", ondelete="CASCADE"), nullable=False
    )
    statut: Mapped[str] = mapped_column(String, nullable=False, default="non_commence")
    derniere_consultation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="progression")


# ============================================================
# 4. ASSISTANT IA
# ============================================================

class ConversationIA(Base):
    __tablename__ = "conversations_ia"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    chapitre_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chapitres.id")
    )
    titre: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = created_at_col()

    messages: Mapped[list["MessageIA"]] = relationship(back_populates="conversation")


class MessageIA(Base):
    __tablename__ = "messages_ia"
    __table_args__ = (
        CheckConstraint("role IN ('utilisateur','assistant')", name="ck_messages_ia_role"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations_ia.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String, nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = created_at_col()

    conversation: Mapped["ConversationIA"] = relationship(back_populates="messages")


class CorrectionDissertation(Base):
    """V2"""
    __tablename__ = "corrections_dissertation"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    matiere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matieres.id"), nullable=False
    )
    texte_soumis: Mapped[str] = mapped_column(Text, nullable=False)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    note_estimee: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2))
    created_at: Mapped[datetime] = created_at_col()


# ============================================================
# 5. CALENDRIER, ACTUALITÉS ET RÉSULTATS
# ============================================================

class EvenementCalendrier(Base):
    __tablename__ = "evenements_calendrier"
    __table_args__ = (
        CheckConstraint(
            "type IN ('rentree','examen','composition','conge','concours','resultat')",
            name="ck_evenements_type",
        ),
        CheckConstraint(
            "statut_fiabilite IN ('a_valider','confirme')", name="ck_evenements_fiabilite"
        ),
        CheckConstraint("cree_par IN ('admin','scraper')", name="ck_evenements_cree_par"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    titre: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    niveau_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id")
    )  # NULL = concerne tous les niveaux
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[Optional[date]] = mapped_column(Date)
    statut_fiabilite: Mapped[str] = mapped_column(String, nullable=False, default="a_valider")
    source: Mapped[Optional[str]] = mapped_column(String)
    cree_par: Mapped[str] = mapped_column(String, nullable=False, default="admin")
    valide_par_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id")
    )
    created_at: Mapped[datetime] = created_at_col()

    rappels: Mapped[list["AbonnementRappel"]] = relationship(back_populates="evenement")


class Actualite(Base):
    __tablename__ = "actualites"
    __table_args__ = (
        CheckConstraint(
            "categorie IN ('officiel','concours','vie_scolaire')", name="ck_actualites_categorie"
        ),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    titre: Mapped[str] = mapped_column(String, nullable=False)
    resume: Mapped[str] = mapped_column(Text, nullable=False)
    lien_source: Mapped[str] = mapped_column(String, nullable=False)
    categorie: Mapped[str] = mapped_column(String, nullable=False)
    date_publication: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    evenement_lie_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evenements_calendrier.id")
    )


class ProfilExamen(Base):
    __tablename__ = "profils_examen"
    __table_args__ = (
        CheckConstraint(
            "examen_suivi IN ('CEPD','BEPC','BAC1','BAC2')", name="ck_profil_examen_type"
        ),
    )

    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), primary_key=True
    )
    numero_table: Mapped[Optional[str]] = mapped_column(String)
    examen_suivi: Mapped[Optional[str]] = mapped_column(String)
    session_annee: Mapped[Optional[int]] = mapped_column(Integer)

    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="profil_examen")


class AbonnementRappel(Base):
    __tablename__ = "abonnements_rappel"
    __table_args__ = (
        CheckConstraint("delai IN ('j7','j1','jour_j')", name="ck_rappel_delai"),
        UniqueConstraint("utilisateur_id", "evenement_id", "delai", name="uq_rappel"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    evenement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evenements_calendrier.id", ondelete="CASCADE"), nullable=False
    )
    delai: Mapped[str] = mapped_column(String, nullable=False)
    envoye: Mapped[bool] = mapped_column(default=False, nullable=False)

    evenement: Mapped["EvenementCalendrier"] = relationship(back_populates="rappels")


class DeviceToken(Base):
    __tablename__ = "device_tokens"
    __table_args__ = (
        CheckConstraint("plateforme IN ('android','ios')", name="ck_device_plateforme"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    token_fcm: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    plateforme: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = created_at_col()

    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="device_tokens")


class NotificationEnvoyee(Base):
    __tablename__ = "notifications_envoyees"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    titre: Mapped[str] = mapped_column(String, nullable=False)
    corps: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    envoye_at: Mapped[datetime] = created_at_col()
    lu: Mapped[bool] = mapped_column(default=False, nullable=False)


# ============================================================
# 6. PAIEMENT ET ABONNEMENT
# ============================================================

class Abonnement(Base):
    __tablename__ = "abonnements"
    __table_args__ = (
        CheckConstraint("type IN ('matiere','niveau_complet')", name="ck_abonnement_type"),
        CheckConstraint("statut IN ('actif','expire','annule')", name="ck_abonnement_statut"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
    matiere_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matieres.id")
    )
    niveau_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id")
    )
    statut: Mapped[str] = mapped_column(String, nullable=False, default="actif")
    date_debut: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    date_fin: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="abonnements")
    transactions: Mapped[list["TransactionPaiement"]] = relationship(back_populates="abonnement")


class TransactionPaiement(Base):
    """fournisseur : agrégateur mobile money togolais (ex. 'paygate', 'cinetpay')."""
    __tablename__ = "transactions_paiement"
    __table_args__ = (
        CheckConstraint("moyen_paiement IN ('tmoney','flooz')", name="ck_transaction_moyen"),
        CheckConstraint(
            "statut IN ('en_attente','confirme','echoue')", name="ck_transaction_statut"
        ),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    abonnement_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("abonnements.id")
    )
    montant: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    devise: Mapped[str] = mapped_column(String, nullable=False, default="XOF")
    moyen_paiement: Mapped[str] = mapped_column(String, nullable=False)
    fournisseur: Mapped[str] = mapped_column(String, nullable=False)
    reference_externe: Mapped[Optional[str]] = mapped_column(String)
    statut: Mapped[str] = mapped_column(String, nullable=False, default="en_attente")
    callback_recu_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = created_at_col()

    abonnement: Mapped[Optional["Abonnement"]] = relationship(back_populates="transactions")


# ============================================================
# 7. MARKETPLACE ENSEIGNANTS — V2
# ============================================================

class Enseignant(Base):
    __tablename__ = "enseignants"
    __table_args__ = (
        CheckConstraint(
            "statut_verification IN ('en_attente','verifie','rejete')", name="ck_enseignant_statut"
        ),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    bio: Mapped[Optional[str]] = mapped_column(Text)
    statut_verification: Mapped[str] = mapped_column(String, nullable=False, default="en_attente")
    created_at: Mapped[datetime] = created_at_col()

    offres: Mapped[list["OffreEnseignant"]] = relationship(back_populates="enseignant")


class OffreEnseignant(Base):
    __tablename__ = "offres_enseignant"

    id: Mapped[uuid.UUID] = uuid_pk()
    enseignant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("enseignants.id", ondelete="CASCADE"), nullable=False
    )
    titre: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    prix: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    matiere_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("matieres.id")
    )
    niveau_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("niveaux.id")
    )
    created_at: Mapped[datetime] = created_at_col()

    enseignant: Mapped["Enseignant"] = relationship(back_populates="offres")


class AbonnementOffre(Base):
    __tablename__ = "abonnements_offre"
    __table_args__ = (
        CheckConstraint("statut IN ('actif','expire','annule')", name="ck_abonnement_offre_statut"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    offre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offres_enseignant.id", ondelete="CASCADE"), nullable=False
    )
    statut: Mapped[str] = mapped_column(String, nullable=False, default="actif")
    date_debut: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    date_fin: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


# ============================================================
# 8. GAMIFICATION — V2
# ============================================================

class Defi(Base):
    __tablename__ = "defis"

    id: Mapped[uuid.UUID] = uuid_pk()
    chapitre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chapitres.id", ondelete="CASCADE"), nullable=False
    )
    titre: Mapped[str] = mapped_column(String, nullable=False)
    duree_secondes: Mapped[int] = mapped_column(Integer, nullable=False)
    questions_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = created_at_col()

    resultats: Mapped[list["ResultatDefi"]] = relationship(back_populates="defi")


class ResultatDefi(Base):
    __tablename__ = "resultats_defi"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False
    )
    defi_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("defis.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    temps_ecoule_secondes: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = created_at_col()

    defi: Mapped["Defi"] = relationship(back_populates="resultats")


# ============================================================
# 9. ADMINISTRATION
# ============================================================

class LogModeration(Base):
    __tablename__ = "logs_moderation"

    id: Mapped[uuid.UUID] = uuid_pk()
    utilisateur_admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False
    )
    cible_type: Mapped[str] = mapped_column(String, nullable=False)
    cible_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    action: Mapped[str] = mapped_column(String, nullable=False)
    commentaire: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = created_at_col()
