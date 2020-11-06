import {Component, Inject, OnInit} from '@angular/core';
import {Baby, Parent} from "../../openapi/models";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {Storage} from "@ionic/storage";

@Component({
    selector: 'app-baby-dialog',
    templateUrl: './baby-dialog.component.html',
    styleUrls: ['./baby-dialog.component.scss'],
})
export class BabyDialogComponent implements OnInit {
    public baby: Baby
    private parent: Parent;

    constructor(
        public dialogRef: MatDialogRef<BabyDialogComponent>,
        @Inject(MAT_DIALOG_DATA) public data: Baby,
        private storage: Storage,
    ) {
        this.baby = new class implements Baby {
            birthDate: Date = new Date();
            fatherId: number;
            id: number;
            motherId: number;
            name: string;
        }
    }

    onCancel(): void {
        this.dialogRef.close()
    }

    async ngOnInit() {
        await this.storage.ready()
        this.parent = await this.storage.get("self")
    }

    parentChosen(parent: string) {
        if(parent ==="father") {
            this.baby.fatherId = this.parent.id
            this.baby.motherId = null
        } else {
            this.baby.fatherId = null
            this.baby.motherId = this.parent.id
        }
    }
}