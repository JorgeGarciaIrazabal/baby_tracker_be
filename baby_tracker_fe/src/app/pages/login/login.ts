import {Component, OnInit} from "@angular/core";
import {NavController, ToastController} from "@ionic/angular";
import {Parent, ParentToJSON} from "../../../openapi/models";
import {ApiService} from "../../api.service";
import { Storage } from '@ionic/storage';


@Component({
    selector: 'page-login',
    templateUrl: 'login.html',
    styleUrls: ['login.scss'],
})
export class LoginPage {
    private user: Parent;
    private signingIn: boolean;

    constructor(public nav: NavController,
                public toastCtrl: ToastController,
                public apiService: ApiService,
                private storage: Storage
    ) {
        this.user = new class implements Parent {
            email: string = "";
            id: number;
            name: string = "";
            password: string = ""
        }
        this.signingIn = true
    }

    async ngOnInit() {
        await this.storage.ready()
        let loggedParent =  this.storage.get("self")
        if le
    }


    async login() {
        try {
            let loggedParent: Parent
            if (this.signingIn) {
                loggedParent = await this.apiService.api.signInSignInPut({
                    email: this.user.email,
                    password: this.user.password
                })
            } else {
                loggedParent = await this.apiService.api.createParentParentPost({parent: this.user})
            }
            let t = await this.toastCtrl.create({
                message: 'Successfully logged in',
            })
            await this.storage.set("self", loggedParent)
            await this.nav.navigateRoot("tabs/timeline");
            await t.present()
        } catch (e) {
            let t = await this.toastCtrl.create({
                message: 'failed logging in :(',
            })
            await t.present()
        }
    }
}
