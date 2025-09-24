import { Routes } from '@angular/router';

import { Home } from './home/home';
import { About } from './about/about';
import { PageNotFound } from './page-not-found/page-not-found';
import { AppFeature } from './app-feature/app-feature';
import { authenGuard } from './core/guards/authen-guard';

export const routes: Routes = [
    {
        path: '',
        component: Home,
    },
    {
        path: 'about',
        component: About,
    },
    {
        path: 'app',
        component: AppFeature,
        canActivate: [authenGuard]
    },
    {
        path:'**', 
        component: PageNotFound
    }
];