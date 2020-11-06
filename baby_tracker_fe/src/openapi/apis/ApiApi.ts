/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import {
    Baby,
    BabyFromJSON,
    BabyToJSON,
    Feed,
    FeedFromJSON,
    FeedToJSON,
    HTTPValidationError,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    Parent,
    ParentFromJSON,
    ParentToJSON,
} from '../models';

export interface CreateBabyBabyPostRequest {
    baby: Baby;
}

export interface CreateParentParentPostRequest {
    parent: Parent;
}

export interface GetBabyFeedsBabyBabyIdFeedsGetRequest {
    babyId: number;
}

export interface GetParentParentIdGetRequest {
    id: number;
}

export interface GetParentsBabyBabyParentIdGetRequest {
    id: number;
}

export interface RemoveParentsBabyBabyBabyIdParentParentIdPutRequest {
    babyId: number;
    parentId: number;
}

export interface SignInSignInPutRequest {
    email: string;
    password: string;
}

export interface UpdateBabyBabyIdPutRequest {
    id: number;
    baby: Baby;
}

/**
 * 
 */
export class ApiApi extends runtime.BaseAPI {

    /**
     * Create Baby
     */
    async createBabyBabyPostRaw(requestParameters: CreateBabyBabyPostRequest): Promise<runtime.ApiResponse<Baby>> {
        if (requestParameters.baby === null || requestParameters.baby === undefined) {
            throw new runtime.RequiredError('baby','Required parameter requestParameters.baby was null or undefined when calling createBabyBabyPost.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/baby`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: BabyToJSON(requestParameters.baby),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => BabyFromJSON(jsonValue));
    }

    /**
     * Create Baby
     */
    async createBabyBabyPost(requestParameters: CreateBabyBabyPostRequest): Promise<Baby> {
        const response = await this.createBabyBabyPostRaw(requestParameters);
        return await response.value();
    }

    /**
     * Create Parent
     */
    async createParentParentPostRaw(requestParameters: CreateParentParentPostRequest): Promise<runtime.ApiResponse<Parent>> {
        if (requestParameters.parent === null || requestParameters.parent === undefined) {
            throw new runtime.RequiredError('parent','Required parameter requestParameters.parent was null or undefined when calling createParentParentPost.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/parent`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: ParentToJSON(requestParameters.parent),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => ParentFromJSON(jsonValue));
    }

    /**
     * Create Parent
     */
    async createParentParentPost(requestParameters: CreateParentParentPostRequest): Promise<Parent> {
        const response = await this.createParentParentPostRaw(requestParameters);
        return await response.value();
    }

    /**
     * Get Baby Feeds
     */
    async getBabyFeedsBabyBabyIdFeedsGetRaw(requestParameters: GetBabyFeedsBabyBabyIdFeedsGetRequest): Promise<runtime.ApiResponse<Array<Feed>>> {
        if (requestParameters.babyId === null || requestParameters.babyId === undefined) {
            throw new runtime.RequiredError('babyId','Required parameter requestParameters.babyId was null or undefined when calling getBabyFeedsBabyBabyIdFeedsGet.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/baby/{baby_id}/feeds`.replace(`{${"baby_id"}}`, encodeURIComponent(String(requestParameters.babyId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(FeedFromJSON));
    }

    /**
     * Get Baby Feeds
     */
    async getBabyFeedsBabyBabyIdFeedsGet(requestParameters: GetBabyFeedsBabyBabyIdFeedsGetRequest): Promise<Array<Feed>> {
        const response = await this.getBabyFeedsBabyBabyIdFeedsGetRaw(requestParameters);
        return await response.value();
    }

    /**
     * Get Parent
     */
    async getParentParentIdGetRaw(requestParameters: GetParentParentIdGetRequest): Promise<runtime.ApiResponse<Parent>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling getParentParentIdGet.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/parent/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => ParentFromJSON(jsonValue));
    }

    /**
     * Get Parent
     */
    async getParentParentIdGet(requestParameters: GetParentParentIdGetRequest): Promise<Parent> {
        const response = await this.getParentParentIdGetRaw(requestParameters);
        return await response.value();
    }

    /**
     * Get Parents Baby
     */
    async getParentsBabyBabyParentIdGetRaw(requestParameters: GetParentsBabyBabyParentIdGetRequest): Promise<runtime.ApiResponse<Baby>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling getParentsBabyBabyParentIdGet.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/baby/parent/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => BabyFromJSON(jsonValue));
    }

    /**
     * Get Parents Baby
     */
    async getParentsBabyBabyParentIdGet(requestParameters: GetParentsBabyBabyParentIdGetRequest): Promise<Baby> {
        const response = await this.getParentsBabyBabyParentIdGetRaw(requestParameters);
        return await response.value();
    }

    /**
     * Get Parents
     */
    async getParentsParentGetRaw(): Promise<runtime.ApiResponse<Array<Parent>>> {
        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/parent`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(ParentFromJSON));
    }

    /**
     * Get Parents
     */
    async getParentsParentGet(): Promise<Array<Parent>> {
        const response = await this.getParentsParentGetRaw();
        return await response.value();
    }

    /**
     * Remove Parents Baby
     */
    async removeParentsBabyBabyBabyIdParentParentIdPutRaw(requestParameters: RemoveParentsBabyBabyBabyIdParentParentIdPutRequest): Promise<runtime.ApiResponse<Baby>> {
        if (requestParameters.babyId === null || requestParameters.babyId === undefined) {
            throw new runtime.RequiredError('babyId','Required parameter requestParameters.babyId was null or undefined when calling removeParentsBabyBabyBabyIdParentParentIdPut.');
        }

        if (requestParameters.parentId === null || requestParameters.parentId === undefined) {
            throw new runtime.RequiredError('parentId','Required parameter requestParameters.parentId was null or undefined when calling removeParentsBabyBabyBabyIdParentParentIdPut.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/baby/{baby_id}/parent/{parent_id}`.replace(`{${"baby_id"}}`, encodeURIComponent(String(requestParameters.babyId))).replace(`{${"parent_id"}}`, encodeURIComponent(String(requestParameters.parentId))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => BabyFromJSON(jsonValue));
    }

    /**
     * Remove Parents Baby
     */
    async removeParentsBabyBabyBabyIdParentParentIdPut(requestParameters: RemoveParentsBabyBabyBabyIdParentParentIdPutRequest): Promise<Baby> {
        const response = await this.removeParentsBabyBabyBabyIdParentParentIdPutRaw(requestParameters);
        return await response.value();
    }

    /**
     * Sign In
     */
    async signInSignInPutRaw(requestParameters: SignInSignInPutRequest): Promise<runtime.ApiResponse<Parent>> {
        if (requestParameters.email === null || requestParameters.email === undefined) {
            throw new runtime.RequiredError('email','Required parameter requestParameters.email was null or undefined when calling signInSignInPut.');
        }

        if (requestParameters.password === null || requestParameters.password === undefined) {
            throw new runtime.RequiredError('password','Required parameter requestParameters.password was null or undefined when calling signInSignInPut.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        if (requestParameters.email !== undefined) {
            queryParameters['email'] = requestParameters.email;
        }

        if (requestParameters.password !== undefined) {
            queryParameters['password'] = requestParameters.password;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/sign_in`,
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => ParentFromJSON(jsonValue));
    }

    /**
     * Sign In
     */
    async signInSignInPut(requestParameters: SignInSignInPutRequest): Promise<Parent> {
        const response = await this.signInSignInPutRaw(requestParameters);
        return await response.value();
    }

    /**
     * Update Baby
     */
    async updateBabyBabyIdPutRaw(requestParameters: UpdateBabyBabyIdPutRequest): Promise<runtime.ApiResponse<Baby>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling updateBabyBabyIdPut.');
        }

        if (requestParameters.baby === null || requestParameters.baby === undefined) {
            throw new runtime.RequiredError('baby','Required parameter requestParameters.baby was null or undefined when calling updateBabyBabyIdPut.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/baby/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: BabyToJSON(requestParameters.baby),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => BabyFromJSON(jsonValue));
    }

    /**
     * Update Baby
     */
    async updateBabyBabyIdPut(requestParameters: UpdateBabyBabyIdPutRequest): Promise<Baby> {
        const response = await this.updateBabyBabyIdPutRaw(requestParameters);
        return await response.value();
    }

}
