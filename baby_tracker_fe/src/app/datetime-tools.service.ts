import { Injectable } from '@angular/core';
// @ts-ignore
import moment from "moment";
import {Feed} from "../openapi/models";

@Injectable({
  providedIn: 'root'
})
export class DatetimeToolsService {

  constructor() { }

  datetimeUIToUtc(date: Date, time: string) {
    let hour = parseInt(time.split(" ")[0].split(":")[0])
    hour = time.split(" ")[1] == "PM" ? 12 + hour : hour
    let min = parseInt(time.split(" ")[0].split(":")[1])
    let momentDate = moment(date)
    momentDate.hours(hour)
    momentDate.minutes(min)
    return momentDate.utc().toDate()
  }

  datetimeToStrTime(date: Date) {
    let momentDate = moment(date)
    return momentDate.format("hh:mm a").toUpperCase()
  }

  dateDiffMin(feed: Feed) {
    if (feed.endAt == null) {
      return 0
    }
    // @ts-ignore
    let diffMs: number = (feed.endAt - feed.startAt); // milliseconds
    return Math.floor(diffMs / 60000)
  }

  dateToUtc(date) {
    return moment(date).utc().toDate()
  }
}
