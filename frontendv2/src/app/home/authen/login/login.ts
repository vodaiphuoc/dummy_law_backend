import { Component, output } from '@angular/core';

@Component({
    selector: 'app-login',
    imports: [],
    templateUrl: './login.html',
    styleUrl: './login.css',
})
export class Login {
    showRegister = output();
}
