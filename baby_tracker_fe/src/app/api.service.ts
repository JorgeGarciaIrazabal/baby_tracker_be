import {Injectable} from '@angular/core';
import {ApiApi} from "../openapi/apis";
import {Configuration} from "../openapi";

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    public api: ApiApi;

    constructor() {
        this.api = new ApiApi(new Configuration({
                basePath: "",
            })
        )
    }
}
