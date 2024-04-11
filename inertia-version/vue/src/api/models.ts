export type Body_api_login_api_login_post = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

export type NewPassword = {
  token: string
  password: string
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UserCreate = {
  email: string
  username: string
  first_name?: string | null
  last_name?: string | null
  password: string
  avatar_url?: Blob | File | null
}

export type UserOut = {
  email: string
  username: string
  first_name?: string | null
  last_name?: string | null
  id: number
  is_active: boolean
  avatar_url?: string | null
}

export type UserUpdate = {
  email?: string | null
  password?: string | null
  first_name?: string | null
  last_name?: string | null
  avatar_url?: Blob | File | null
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}
