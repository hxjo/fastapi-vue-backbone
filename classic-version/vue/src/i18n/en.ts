import type { TranslationRecord } from './types'

export const EnglishTranslationRecord: TranslationRecord = {
  auth: {
    signUp: {
      header: 'Create an account',
      subheader: 'Enter your email to create an account'
    },
    logIn: {
      header: 'Log in',
      subheader: 'Enter your credentials to log in',
      button: 'Log in'
    },
    recoverPassword: {
      header: 'Recover password',
      subheader: 'Enter your email to recover your password',
      button: 'Send recovery email'
    },
    resetPassword: {
      header: 'Reset password for email {email}',
      subheader: 'Enter your new password',
      button: 'Reset password'
    },
    logOut: 'Log out',
    email: 'Email',
    password: 'Password',
    passwordConfirm: 'Confirm password',
    errors: {
      email: 'Please enter a valid email',
      passwordMatch: 'Passwords do not match',
      passwordStrength:
        'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character.',
      invalidToken: 'Invalid token'
    },
    success: {
      recoveryEmail: 'Recovery email sent',
      resetPassword: 'Password reset successfully'
    }
  },
  user: {
    profile: 'Profile',
    editProfileModal: {
      header: 'Edit profile',
      avatar: 'Avatar'
    },
    username: 'Username',
    firstName: 'First name',
    lastName: 'Last name',
    success: {
      update: 'User updated successfully'
    }
  },
  forms: {
    continue: 'Continue',
    goBack: 'Go back',
    save: 'Save',
    errors: {
      minLength: 'This field must contain at least {minLength} characters',
      maxLength: 'This field must contain at most {maxLength} characters',
      required: 'Required field',
      maxFileSize: 'Max file size is {maxFileSize}',
      acceptedImageTypes: 'Accepted image types are {acceptedImageTypes}'
    }
  },
  goToApp: 'Go to app',
  welcome: 'Welcome',
  settings: {
    header: 'Settings',
    language: {
      header: 'Language'
    },
    theme: {
      header: 'Theme',
      light: 'Light',
      dark: 'Dark',
      auto: 'Auto'
    }
  },
  serverMessages: {
    auth: {
      invalid: {
        invalid_credentials: 'Invalid credentials',
        password_not_strong: 'Password not strong enough'
      }
    },
    user: {
      conflict: {
        email_already_registered: 'Email already registered'
      },
      invalid: {
        inactive: 'Inactive user'
      }
    },
    internalServerError: 'Internal server error'
  }
}
