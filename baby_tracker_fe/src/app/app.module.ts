import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {RouteReuseStrategy} from '@angular/router';

import {IonicModule, IonicRouteStrategy} from '@ionic/angular';
import {SplashScreen} from '@ionic-native/splash-screen/ngx';
import {StatusBar} from '@ionic-native/status-bar/ngx';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {CommonModule} from "@angular/common";
import {IonicStorageModule} from "@ionic/storage";
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {TestLoginComponent} from './test-login/test-login.component';
import {MatInputModule} from '@angular/material/input';
import {MatButtonModule} from '@angular/material/button';
import {MatSelectModule} from '@angular/material/select';
import {MatRadioModule} from '@angular/material/radio';
import {MatCardModule} from '@angular/material/card';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatButtonToggleModule} from "@angular/material/button-toggle";
import {FrameComponent} from './frame/frame.component';
import {LayoutModule} from '@angular/cdk/layout';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatMenuModule} from '@angular/material/menu';
import {AnalyticsComponent} from './analytics/analytics.component';
import {BabyDialogComponent} from "./baby-dialog/baby-dialog.component";
import {MatDialogModule} from "@angular/material/dialog";
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatNativeDateModule} from "@angular/material/core";
import {TrackTabsComponent} from "./track-tabs/track-tabs.component";
import {MatTabsModule} from "@angular/material/tabs";
import {TrackFeedComponent} from "./track-feed/track-feed.component";
import {FeedDialogComponent} from "./feed-dialog/feed-dialog.component";
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';

@NgModule({
    declarations: [
        AppComponent,
        TestLoginComponent,
        FrameComponent,
        AnalyticsComponent,
        BabyDialogComponent,
        TrackTabsComponent,
        TrackFeedComponent,
        FeedDialogComponent,
    ],
    entryComponents: [],
    imports: [
        BrowserModule,
        IonicModule.forRoot(),
        IonicStorageModule.forRoot(),
        AppRoutingModule,
        HttpClientModule,
        CommonModule,
        BrowserAnimationsModule,
        MatInputModule,
        MatButtonModule,
        MatSelectModule,
        MatRadioModule,
        MatCardModule,
        ReactiveFormsModule,
        MatButtonToggleModule,
        LayoutModule,
        MatToolbarModule,
        MatSidenavModule,
        MatIconModule,
        MatListModule,
        MatGridListModule,
        MatMenuModule,
        MatDialogModule,
        FormsModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatTabsModule,
        NgxMaterialTimepickerModule,
    ],
    providers: [
        StatusBar,
        SplashScreen,
        {provide: RouteReuseStrategy, useClass: IonicRouteStrategy},
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
