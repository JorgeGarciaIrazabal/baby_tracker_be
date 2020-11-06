import {Component} from '@angular/core';
import {ApiApi, Configuration, Parent} from "../../openapi";
import {Observable} from "rxjs";
import {ApiService} from "../api.service";

@Component({
    selector: 'app-tabs',
    templateUrl: 'tabs.page.html',
    styleUrls: ['tabs.page.scss']
})
export class TabsPage {
    private api: ApiApi;
    private parents: Array<Parent> = [];

    constructor(private apiService: ApiService) {
    }

    async ngOnInit() {
        this.parents = await this.apiService.api.getParentsParentGet()
    }
}
