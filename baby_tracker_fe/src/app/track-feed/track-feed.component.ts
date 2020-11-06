import {Component, Input, OnInit} from '@angular/core';
import {Baby, Feed, FeedTypes, Parent} from "../../openapi/models";
import {ApiService} from "../api.service";
import {MatDialog} from "@angular/material/dialog";
import {FeedDialogComponent} from "../feed-dialog/feed-dialog.component";

@Component({
  selector: 'app-track-feed',
  templateUrl: './track-feed.component.html',
  styleUrls: ['./track-feed.component.scss'],
})
export class TrackFeedComponent implements OnInit {

  @Input() parent: Parent
  @Input() baby: Baby
  public feeds: Array<Feed>
  constructor( private apiService: ApiService, public dialog: MatDialog) { }

  async ngOnInit() {
    this.feeds = await this.apiService.api.getBabyFeedsBabyBabyIdFeedsGet({babyId: this.baby.id})
  }

  dateDiffMin(feed:Feed) {
    if (feed.endAt == null) {
      return 0
    }
    // @ts-ignore
    let diffMs: number = (feed.endAt - feed.startAt); // milliseconds
    return Math.floor(diffMs/60000)
  }

  async openDialog() {
    let baby = this.baby
    const dialogRef = this.dialog.open(FeedDialogComponent, {
      width: '250px',
      data: new class implements Feed {
        amount: number = 100;
        babyId: number = baby.id;
        endAt: Date = null;
        id: number;
        startAt: Date = new Date();
        type: FeedTypes = FeedTypes.NUMBER_1;
      }
    });

    dialogRef.afterClosed().subscribe(async result => {
      this.feeds.push(result);
    });
  }
}
