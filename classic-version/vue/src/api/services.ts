import type { CancelablePromise } from './core/CancelablePromise'
import { OpenAPI } from './core/OpenAPI'
import { request as __request } from './core/request'

import type {
  Body_api_login_api_login_post,
  NewPassword,
  Token,
  UserOut,
  UserCreate,
  UserUpdate
} from './models'

export type LoginData = {
  ApiLoginApiLoginPost: {
    formData: Body_api_login_api_login_post
  }
  RecoverPasswordPasswordRecoveryEmailPost: {
    email: string
  }
  ResetPasswordResetPasswordPost: {
    requestBody: NewPassword
  }
  RecoverPasswordViewRecoverPasswordGet: {
    token: string
  }
}

export type UsersData = {
  CreateUserApiV1UsersPost: {
    requestBody: UserCreate
  }
  SearchUsersApiV1UsersGet: {
    offset?: number
    query?: string
  }
  GetUserByIdApiV1UsersUserIdGet: {
    userId: number
  }
  UpdateUserApiV1UsersUserIdPatch: {
    requestBody: UserUpdate
    userId: number
  }
  DeleteUserApiV1UsersUserIdDelete: {
    userId: number
  }
}

export class LoginService {
  /**
   * Api Login
   * @returns Token Successful Response
   * @throws ApiError
   */
  public static apiLoginApiLoginPost(
    data: LoginData['ApiLoginApiLoginPost']
  ): CancelablePromise<Token> {
    const { formData } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/login',
      formData: formData,
      mediaType: 'application/x-www-form-urlencoded',
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Recover Password
   * @returns void Successful Response
   * @throws ApiError
   */
  public static recoverPasswordPasswordRecoveryEmailPost(
    data: LoginData['RecoverPasswordPasswordRecoveryEmailPost']
  ): CancelablePromise<void> {
    const { email } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/password/recovery/{email}',
      path: {
        email
      },
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Reset Password
   * Reset password
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static resetPasswordResetPasswordPost(
    data: LoginData['ResetPasswordResetPasswordPost']
  ): CancelablePromise<UserOut> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/reset-password/',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Recover Password View
   * @returns unknown Successful Response
   * @throws ApiError
   */
  public static recoverPasswordViewRecoverPasswordGet(
    data: LoginData['RecoverPasswordViewRecoverPasswordGet']
  ): CancelablePromise<unknown> {
    const { token } = data
    return __request(OpenAPI, {
      method: 'GET',
      url: '/recover-password',
      query: {
        token
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
}

export class UsersService {
  /**
   * Create User
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static createUserApiV1UsersPost(
    data: UsersData['CreateUserApiV1UsersPost']
  ): CancelablePromise<UserOut> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/v1/users/',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Search Users
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static searchUsersApiV1UsersGet(
    data: UsersData['SearchUsersApiV1UsersGet'] = {}
  ): CancelablePromise<Array<UserOut>> {
    const { query = '', offset = 0 } = data
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/users/',
      query: {
        query,
        offset
      },
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Get User Me
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static getUserMeApiV1UsersMeGet(): CancelablePromise<UserOut> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/users/me'
    })
  }

  /**
   * Get User By Id
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static getUserByIdApiV1UsersUserIdGet(
    data: UsersData['GetUserByIdApiV1UsersUserIdGet']
  ): CancelablePromise<UserOut> {
    const { userId } = data
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/users/{user_id}',
      path: {
        user_id: userId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Update User
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static updateUserApiV1UsersUserIdPatch(
    data: UsersData['UpdateUserApiV1UsersUserIdPatch']
  ): CancelablePromise<UserOut> {
    const { userId, requestBody } = data
    return __request(OpenAPI, {
      method: 'PATCH',
      url: '/api/v1/users/{user_id}',
      path: {
        user_id: userId
      },
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }

  /**
   * Delete User
   * @returns void Successful Response
   * @throws ApiError
   */
  public static deleteUserApiV1UsersUserIdDelete(
    data: UsersData['DeleteUserApiV1UsersUserIdDelete']
  ): CancelablePromise<void> {
    const { userId } = data
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/api/v1/users/{user_id}',
      path: {
        user_id: userId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
}
