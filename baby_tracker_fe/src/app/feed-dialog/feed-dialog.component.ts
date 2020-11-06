import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {Baby, Feed, FeedTypes} from "../../openapi/models";
import {Storage} from "@ionic/storage";

@Component({
  selector: 'app-feed-dialog',
  templateUrl: './feed-dialog.component.html',
  styleUrls: ['./feed-dialog.component.scss'],
})
export class FeedDialogComponent implements OnInit {
  public feed: Feed;

  constructor(
      public dialogRef: MatDialogRef<FeedDialogComponent>,
      @Inject(MAT_DIALOG_DATA) public data: Feed,
  ) {
    this.feed = data
  }

  onCancel(): void {
    this.dialogRef.close()
  }

  ngOnInit() {}


}
