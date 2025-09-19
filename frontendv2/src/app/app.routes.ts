import { Routes } from '@angular/router';

import { Home  } from './home/home';
import { AppFeature } from './app-feature/app-feature';
import { ContentDelivery } from './content-delivery/content-delivery';
import { ProductDetailComponent } from './content-delivery/product-detail/product-detail';
import { ProductListComponent } from './content-delivery/product-list/product-list'

export const routes: Routes = [
    {
        path: '',
        component: Home,
    },
    {
        path: 'app',
        component: AppFeature,
        children: [
            {
                path: '',
                component: ContentDelivery,
                children: [
                    {
                        path: 'products',
                        component: ProductListComponent
                    },
                    {
                        path: 'products/:id',
                        component: ProductDetailComponent
                    }
                ]
            },
            
        ]
    }
];