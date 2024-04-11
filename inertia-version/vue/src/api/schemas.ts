export const $Body_api_login_api_login_post = {
  properties: {
    grant_type: {
      type: 'any-of',
      contains: [
        {
          type: 'string',
          pattern: 'password'
        },
        {
          type: 'null'
        }
      ]
    },
    username: {
      type: 'string',
      isRequired: true
    },
    password: {
      type: 'string',
      isRequired: true
    },
    scope: {
      type: 'string',
      default: ''
    },
    client_id: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    },
    client_secret: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    }
  }
} as const

export const $HTTPValidationError = {
  properties: {
    detail: {
      type: 'array',
      contains: {
        type: 'ValidationError'
      }
    }
  }
} as const

export const $NewPassword = {
  properties: {
    token: {
      type: 'string',
      isRequired: true
    },
    password: {
      type: 'string',
      isRequired: true
    }
  }
} as const

export const $Token = {
  properties: {
    access_token: {
      type: 'string',
      isRequired: true
    },
    token_type: {
      type: 'string',
      default: 'bearer'
    }
  }
} as const

export const $UserCreate = {
  properties: {
    email: {
      type: 'string',
      isRequired: true,
      format: 'email'
    },
    username: {
      type: 'string',
      isRequired: true
    },
    password: {
      type: 'string',
      isRequired: true
    },
    avatar_url: {
      type: 'any-of',
      contains: [
        {
          type: 'binary',
          format: 'binary'
        },
        {
          type: 'null'
        }
      ]
    }
  }
} as const

export const $UserOut = {
  properties: {
    email: {
      type: 'string',
      isRequired: true,
      format: 'email'
    },
    username: {
      type: 'string',
      isRequired: true
    },
    id: {
      type: 'number',
      isRequired: true
    },
    is_active: {
      type: 'boolean',
      isRequired: true
    },
    avatar_url: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    }
  }
} as const

export const $UserUpdate = {
  properties: {
    email: {
      type: 'any-of',
      contains: [
        {
          type: 'string',
          format: 'email'
        },
        {
          type: 'null'
        }
      ]
    },
    password: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    },
    first_name: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    },
    last_name: {
      type: 'any-of',
      contains: [
        {
          type: 'string'
        },
        {
          type: 'null'
        }
      ]
    },
    avatar_url: {
      type: 'any-of',
      contains: [
        {
          type: 'binary',
          format: 'binary'
        },
        {
          type: 'null'
        }
      ]
    }
  }
} as const

export const $ValidationError = {
  properties: {
    loc: {
      type: 'array',
      contains: {
        type: 'any-of',
        contains: [
          {
            type: 'string'
          },
          {
            type: 'number'
          }
        ]
      },
      isRequired: true
    },
    msg: {
      type: 'string',
      isRequired: true
    },
    type: {
      type: 'string',
      isRequired: true
    }
  }
} as const
