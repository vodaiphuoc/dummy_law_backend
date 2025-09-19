import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { makeStateKey, TransferState } from '@angular/core';
import { isPlatformServer } from '@angular/common';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

const PRODUCTS_KEY = makeStateKey<any>('products');

@Injectable({ providedIn: 'root' })
export class ProductService {
    constructor(
        private http: HttpClient,
        private state: TransferState,
        @Inject(PLATFORM_ID) private platformId: Object
    ) {}

    getProducts(): Observable<any> {
        const saved = this.state.get(PRODUCTS_KEY, null);
        if (saved) {
            return of(saved);
        }

        return this.http.get('/api/products').pipe(
            tap(data => {
                if (isPlatformServer(this.platformId)) {
                    this.state.set(PRODUCTS_KEY, data);
                }
                console.log('result of loda data:', data);
            })
        );
    }
}
