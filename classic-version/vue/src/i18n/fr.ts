import type { TranslationRecord } from './types'

export const FrenchTranslationRecord: TranslationRecord = {
  auth: {
    signUp: {
      header: 'Créer un compte',
      subheader: 'Entrez votre email afin de créer un compte'
    },
    logIn: {
      header: 'Se connecter',
      subheader: 'Entrez vos identifiants pour vous connecter',
      button: 'Se connecter'
    },
    recoverPassword: {
      header: 'Récupérer le mot de passe',
      subheader: 'Entrez votre email pour récupérer votre mot de passe',
      button: 'Envoyer un email de récupération'
    },
    resetPassword: {
      header: "Réinitialiser le mot de passe pour l'email {email}",
      subheader: 'Entrez votre nouveau mot de passe',
      button: 'Réinitialiser le mot de passe'
    },
    logOut: 'Se déconnecter',
    email: 'Email',
    password: 'Mot de passe',
    passwordConfirm: 'Confirmer le mot de passe',
    errors: {
      email: 'Veuillez entrer un e-mail valide',
      passwordMatch: 'Les mots de passe ne correspondent pas',
      passwordStrength:
        'Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial.',
      invalidToken: 'Token invalide'
    },
    success: {
      recoveryEmail: 'Email de récupération envoyé',
      resetPassword: 'Mot de passe réinitialisé'
    }
  },
  user: {
    profile: 'Profil',
    editProfileModal: {
      header: 'Modifier le profil',
      avatar: 'Avatar'
    },
    username: "Nom d'utilisateur",
    firstName: 'Prénom',
    lastName: 'Nom de famille',
    success: {
      update: 'Utilisateur mis à jour avec succès'
    }
  },
  forms: {
    continue: 'Continuer',
    goBack: 'Retour',
    save: 'Sauvegarder',
    errors: {
      minLength: 'Ce champ doit contenir au moins {minLength} caractères',
      maxLength: 'Ce champ doit contenir au plus {maxLength} caractères',
      required: 'Champ obligatoire',
      maxFileSize: 'La taille maximale du fichier est de {maxFileSize}',
      acceptedImageTypes: "Les types d'image acceptés sont {acceptedImageTypes}"
    }
  },
  goToApp: "Aller à l'application",
  welcome: 'Bienvenue',
  settings: {
    header: 'Paramètres',
    language: {
      header: 'Langue'
    },
    theme: {
      header: 'Thème',
      light: 'Clair',
      dark: 'Sombre',
      auto: 'Auto'
    }
  },
  serverMessages: {
    auth: {
      invalid: {
        invalid_credentials: 'Identifiants invalides',
        password_not_strong: 'Mot de passe pas assez fort'
      }
    },
    user: {
      conflict: {
        email_already_registered: 'Email déjà enregistré'
      },
      invalid: {
        inactive: 'Utilisateur inactif'
      }
    },
    internalServerError: 'Erreur interne du serveur'
  }
}
