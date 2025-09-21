import { Routes } from '@angular/router';

import { Home  } from './home/home';
import { AppFeature } from './app-feature/app-feature';
import { authenGuard } from './core/guards/authen-guard';

export const routes: Routes = [
    {
        path: '',
        component: Home,
    },
    {
        path: 'app',
        component: AppFeature,
        canActivate: [authenGuard]
    }

];