export interface TranslationRecord {
  auth: {
    signUp: {
      header: string
      subheader: string
    }
    logIn: {
      header: string
      subheader: string
      button: string
    }
    recoverPassword: {
      header: string
      subheader: string
      button: string
    }
    resetPassword: {
      header: string
      subheader: string
      button: string
    }
    logOut: string
    email: string
    password: string
    passwordConfirm: string
    errors: {
      email: string
      passwordMatch: string
      passwordStrength: string
      invalidToken: string
    }
    success: {
      recoveryEmail: string
      resetPassword: string
    }
  }
  user: {
    profile: string
    editProfileModal: {
      header: string
      avatar: string
    }
    username: string
    firstName: string
    lastName: string
    success: {
      update: string
    }
  }
  forms: {
    continue: string
    save: string
    goBack: string
    errors: {
      minLength: string
      maxLength: string
      required: string
      maxFileSize: string
      acceptedImageTypes: string
    }
  }
  goToApp: string
  welcome: string
  settings: {
    header: string
    language: {
      header: string
    }
    theme: {
      header: string
      light: string
      dark: string
      auto: string
    }
  }
  serverMessages: {
    auth: {
      invalid: {
        invalid_credentials: string
        password_not_strong: string
      }
    }
    user: {
      conflict: {
        email_already_registered: string
      }
      invalid: {
        inactive: string
      }
    }
    internalServerError: string
  }
}
