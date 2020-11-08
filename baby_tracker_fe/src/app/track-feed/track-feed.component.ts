import {Component, Input, OnInit} from '@angular/core';
import {Baby, Feed, FeedTypes, Parent} from "../../openapi/models";
import {ApiService} from "../api.service";
import {MatDialog} from "@angular/material/dialog";
import {ToastController} from "@ionic/angular";
import {DatetimeToolsService} from "../datetime-tools.service";

@Component({
    selector: 'app-track-feed',
    templateUrl: './track-feed.component.html',
    styleUrls: ['./track-feed.component.scss'],
})
export class TrackFeedComponent implements OnInit {

    @Input() parent: Parent
    @Input() baby: Baby
    public feeds: Array<Feed>
    public editingFeed: number = null

    constructor(private apiService: ApiService, public dialog: MatDialog,
                public toastCtrl: ToastController, public dtt: DatetimeToolsService) {
    }

    async ngOnInit() {
        this.feeds = await this.apiService.api.getBabyFeedsBabyBabyIdFeedGet({babyId: this.baby.id})
    }

    clearEditingFeed() {
        this.editingFeed = null
        this.feeds = this.feeds.filter((feed) => {
            return feed.id !== -1
        })
    }

    async feedEvent(feed) {
        if (feed.id === -1) {
            await this.createFeed(feed)
        } else {
            await  this.updateFeed(feed)
        }
        this.feeds = await this.apiService.api.getBabyFeedsBabyBabyIdFeedGet({babyId: this.baby.id})
        this.editingFeed = null
    }

    async createFeed(feed) {
        try {
            delete feed.id
            if (feed.endAt === null) {
                delete feed.endAt
            }
            await this.apiService.api.createFeedFeedPost({feed: feed})
        } catch (e) {
            await (await this.toastCtrl.create({
                message: "failed creating feed",
                duration: 1
            })).present()
        }
    }

    async updateFeed(feed) {
        try {
            await this.apiService.api.updateFeedFeedPut({feed: feed})
        } catch (e) {
            await (await this.toastCtrl.create({
                message: "failed updating feed",
                duration: 1
            })).present()
        }
    }

    addEmptyFeed() {
        let baby = this.baby
        let newFeed = new class implements Feed {
            amount: number = 100;
            babyId: number = baby.id;
            endAt: Date = null;
            id: number = -1;
            startAt: Date = new Date();
            type: FeedTypes = FeedTypes.NUMBER_1;
        }
        this.feeds = [
            newFeed,
            ...this.feeds
        ]
        this.editingFeed = -1
    }

    async endFeeding(feed: Feed) {
        feed.endAt = this.dtt.dateToUtc(new Date())
        await this.apiService.api.updateFeedFeedPut({feed: feed})
        this.feeds = await this.apiService.api.getBabyFeedsBabyBabyIdFeedGet({babyId: this.baby.id})
        this.editingFeed = null
    }
}
