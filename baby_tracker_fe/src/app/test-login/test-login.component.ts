import {Component} from '@angular/core';
import {FormBuilder, FormControl, FormGroupDirective, NgForm, Validators} from '@angular/forms';
import {Parent} from "../../openapi/models";
import {NavController, ToastController} from "@ionic/angular";
import {ApiService} from "../api.service";
import {Storage} from "@ionic/storage";


@Component({
    selector: 'app-test-login',
    templateUrl: './test-login.component.html',
    styleUrls: ['./test-login.component.css']
})
export class TestLoginComponent {
    parentForm = this.fb.group({
        name: null,
        email: [null, Validators.required],
        password: [null, Validators.required],
        signingUp: [false]
    });
    public signingUp = false

    constructor(private fb: FormBuilder,
                public nav: NavController,
                public toastCtrl: ToastController,
                public apiService: ApiService,
                private storage: Storage) {
    }

    async ngOnInit() {
        await this.storage.ready()
        let loggedParent =  await this.storage.get("self")
        if (loggedParent !== null) {
            await this.nav.navigateRoot("tabs/timeline");
        }
    }


    async onSubmit(parent) {
        try {
            let loggedParent: Parent
            if (!this.signingUp) {
                loggedParent = await this.apiService.api.signInSignInPut({
                    email: parent.email,
                    password: parent.password
                })
            } else {
                loggedParent = await this.apiService.api.createParentParentPost({parent: parent})
            }
            let t = await this.toastCtrl.create({
                message: 'Successfully logged in',
            })
            await this.storage.set("self", loggedParent)
            await this.nav.navigateRoot("");
            await t.present()
        } catch (e) {
            let t = await this.toastCtrl.create({
                message: 'failed logging in :(',
            })
            await t.present()
        }
    }
}
