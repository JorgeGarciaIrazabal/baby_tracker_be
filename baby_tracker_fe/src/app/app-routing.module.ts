import {NgModule} from '@angular/core';
import {PreloadAllModules, RouterModule, Routes} from '@angular/router';
import {TestLoginComponent} from "./test-login/test-login.component";
import {FrameComponent} from "./frame/frame.component";

const routes: Routes = [
  {
    path: '',
    component: FrameComponent,
  },
  {
    path: 'login',
    component: TestLoginComponent,
  },
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules }),
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
