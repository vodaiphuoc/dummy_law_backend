import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { RegisterModel } from '../models/register-request';

@Injectable({
    providedIn: 'root'
})
export class AuthenService {
    constructor(private http: HttpClient) {
    }

    registerNewAccount(registerData: RegisterModel) {
        this.http.post('http://127.0.0.1:8080/api/register', registerData)
            .subscribe({
                next: responseData => {
                    console.log(responseData);
                }
            })
    }

    checkTokenExpiration() {
        this.http.get('/api/protected', { withCredentials: true })
            .subscribe({
                next: user => {
                
                },
                error: () => {
                  
                    //   this.redirectToLogin();
                }
            });
    }


}
