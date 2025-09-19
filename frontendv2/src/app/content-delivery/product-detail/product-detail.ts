import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProductService } from '../services/product/product-service';

@Component({
    selector: 'app-product-detail',
    templateUrl: './product-detail.html',
    styleUrl: './product-detail.css'
})
export class ProductDetailComponent implements OnInit {
    product: any;

    constructor(
        private route: ActivatedRoute,
        private productService: ProductService
    ) {}

    ngOnInit() {
        const id = this.route.snapshot.paramMap.get('id');
        this.productService.getProducts().subscribe(products => {
            this.product = products.find((p: any) => p.id == id);
        });
    }
}
