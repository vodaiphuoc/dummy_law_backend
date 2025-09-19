import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ProductService } from '../services/product/product-service';

@Component({
    selector: 'app-product-list',
    imports: [RouterLink],
    templateUrl: './product-list.html',
    styleUrl: './product-list.css'
})
export class ProductListComponent implements OnInit {
    products: any[] = [];
    constructor(private productService: ProductService) {}

    ngOnInit() {
        this.productService.getProducts().subscribe(data => this.products = data);
    }
}
