import { Component, signal, model, computed } from '@angular/core';

import { Login } from './login/login';
import { Register } from './register/register';

@Component({
  selector: 'app-authen',
  imports: [Login, Register],
  templateUrl: './authen.html',
  styleUrl: './authen.css'
})
export class Authen {
    shouldShowLogin = model<boolean>(true);

    setShowLoginFromChildComponents(newState: boolean) {
        this.shouldShowLogin.set(newState);
    }

}
