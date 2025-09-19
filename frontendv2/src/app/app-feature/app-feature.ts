import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { Chat } from '../chat/chat';
import { ContentDelivery } from '../content-delivery/content-delivery'

@Component({
    selector: 'app-app-feature',
    imports: [Chat, ContentDelivery],
    templateUrl: './app-feature.html',
    styleUrl: './app-feature.css'
})
export class AppFeature {
    isBrowser = false;
    constructor(@Inject(PLATFORM_ID) platformId: Object) {
        this.isBrowser = isPlatformBrowser(platformId);
        console.log('in AppFeature: ', this.isBrowser);
    }
}
