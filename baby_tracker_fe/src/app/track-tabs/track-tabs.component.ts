import {Component, Input, OnInit} from '@angular/core';
import {Baby} from "../../openapi/models";

@Component({
  selector: 'app-track-tabs',
  templateUrl: './track-tabs.component.html',
  styleUrls: ['./track-tabs.component.scss'],
})
export class TrackTabsComponent implements OnInit {
  @Input() baby: Baby
  constructor() { }

  ngOnInit() {}
}
