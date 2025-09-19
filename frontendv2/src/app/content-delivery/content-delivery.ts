import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// import { ProductDetailComponent } from './product-detail/product-detail';
import { ProductListComponent } from './product-list/product-list'

@Component({
    selector: 'app-content-delivery',
    imports: [RouterOutlet, ProductListComponent],
    templateUrl: './content-delivery.html',
    styleUrl: './content-delivery.css'
})
export class ContentDelivery {

}
