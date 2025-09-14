import { Component } from '@angular/core';
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
    selector: 'app-add-files',
    imports: [MatButtonModule, MatMenuModule, MatIconModule],
    templateUrl: './add-files.html',
    styleUrl: './add-files.css'
})
export class AddFiles {
    
    constructor(
        private matIconRegistry: MatIconRegistry,
        private domSanitizer: DomSanitizer    
    ) {
        this.matIconRegistry.addSvgIcon(
            'add-file-menu',
            this.domSanitizer.bypassSecurityTrustResourceUrl('/assets/add-files/menu.svg')
        ).addSvgIcon(
            'add-file-icon',
            this.domSanitizer.bypassSecurityTrustResourceUrl('/assets/add-files/attach-file.svg')
        ).addSvgIcon(
            'add-image-icon',
            this.domSanitizer.bypassSecurityTrustResourceUrl('/assets/add-files/add-image.svg')
        );
    }
}
