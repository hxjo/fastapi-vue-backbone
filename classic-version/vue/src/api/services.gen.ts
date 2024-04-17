// This file is auto-generated by @hey-api/openapi-ts

import type { CancelablePromise } from './core/CancelablePromise'
import { OpenAPI } from './core/OpenAPI'
import { request as __request } from './core/request'
import type { $OpenApiTs } from './types.gen'

export class LoginService {
  /**
   * Api Login
   * @returns UserAndToken Successful Response
   * @throws ApiError
   */
  public static apiLoginApiLoginPost(
    data: $OpenApiTs['/api/login']['post']['req']
  ): CancelablePromise<$OpenApiTs['/api/login']['post']['res'][200]> {
    const { formData } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/login',
      formData,
      mediaType: 'application/x-www-form-urlencoded',
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Send Recover Password Email
   * @returns void Successful Response
   * @throws ApiError
   */
  public static sendRecoverPasswordEmailApiRecoverPasswordEmailPost(
    data: $OpenApiTs['/api/recover-password/{email}']['post']['req']
  ): CancelablePromise<$OpenApiTs['/api/recover-password/{email}']['post']['res'][204]> {
    const { email } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/recover-password/{email}',
      path: {
        email
      },
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Reset Password
   * Reset password
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static resetPasswordApiResetPasswordPost(
    data: $OpenApiTs['/api/reset-password/']['post']['req']
  ): CancelablePromise<$OpenApiTs['/api/reset-password/']['post']['res'][201]> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/reset-password/',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: 'Validation Error'
      }
    })
  }
}

export class UsersService {
  /**
   * Create User
   * @returns UserAndToken Successful Response
   * @throws ApiError
   */
  public static createUserApiV1UsersPost(
    data: $OpenApiTs['/api/v1/users/']['post']['req']
  ): CancelablePromise<$OpenApiTs['/api/v1/users/']['post']['res'][201]> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/v1/users/',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Search Users
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static searchUsersApiV1UsersGet(
    data: $OpenApiTs['/api/v1/users/']['get']['req'] = {}
  ): CancelablePromise<$OpenApiTs['/api/v1/users/']['get']['res'][200]> {
    const { query, offset } = data
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/users/',
      query: {
        query,
        offset
      },
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Get User Me
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static getUserMeApiV1UsersMeGet(): CancelablePromise<
    $OpenApiTs['/api/v1/users/me']['get']['res'][200]
  > {
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
    data: $OpenApiTs['/api/v1/users/{user_id}']['get']['req']
  ): CancelablePromise<$OpenApiTs['/api/v1/users/{user_id}']['get']['res'][200]> {
    const { userId } = data
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/users/{user_id}',
      path: {
        user_id: userId
      },
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Update User
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static updateUserApiV1UsersUserIdPatch(
    data: $OpenApiTs['/api/v1/users/{user_id}']['patch']['req']
  ): CancelablePromise<$OpenApiTs['/api/v1/users/{user_id}']['patch']['res'][201]> {
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
        422: 'Validation Error'
      }
    })
  }

  /**
   * Delete User
   * @returns void Successful Response
   * @throws ApiError
   */
  public static deleteUserApiV1UsersUserIdDelete(
    data: $OpenApiTs['/api/v1/users/{user_id}']['delete']['req']
  ): CancelablePromise<$OpenApiTs['/api/v1/users/{user_id}']['delete']['res'][204]> {
    const { userId } = data
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/api/v1/users/{user_id}',
      path: {
        user_id: userId
      },
      errors: {
        422: 'Validation Error'
      }
    })
  }

  /**
   * Set User Avatar
   * @returns UserOut Successful Response
   * @throws ApiError
   */
  public static setUserAvatarApiV1UsersUserIdAvatarPost(
    data: $OpenApiTs['/api/v1/users/{user_id}/avatar']['post']['req']
  ): CancelablePromise<$OpenApiTs['/api/v1/users/{user_id}/avatar']['post']['res'][201]> {
    const { userId, formData } = data
    return __request(OpenAPI, {
      method: 'POST',
      url: '/api/v1/users/{user_id}/avatar',
      path: {
        user_id: userId
      },
      formData,
      mediaType: 'multipart/form-data',
      errors: {
        422: 'Validation Error'
      }
    })
  }
}
