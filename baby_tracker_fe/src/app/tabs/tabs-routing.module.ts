import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {TabsPage} from './tabs.page';
import {LoginPage} from "../pages/login/login";

const routes: Routes = [
    {
        path: 'tabs',
        component: TabsPage,
        children: [
            {
                path: 'profile',
                loadChildren: () => import('../tab1/tab1.module').then(m => m.Tab1PageModule)
            },
            {
                path: 'timeline',
                loadChildren: () => import('../tab2/tab2.module').then(m => m.Tab2PageModule)
            },
            {
                path: 'analytics',
                loadChildren: () => import('../tab3/tab3.module').then(m => m.Tab3PageModule)
            },
            {
                path: '',
                redirectTo: '/tabs/timeline',
                pathMatch: 'full'
            }
        ]
    },
    {
        path: 'login',
        component: LoginPage,
    },
    {
        path: '',
        redirectTo: '/tabs/timeline',
        pathMatch: 'full'
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class TabsPageRoutingModule {
}
