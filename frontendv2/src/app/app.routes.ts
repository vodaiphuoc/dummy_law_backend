import { Routes } from '@angular/router';

import { Home } from './home/home';
import { About } from './about/about';
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
    }

];