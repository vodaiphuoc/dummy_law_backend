import { Component, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { FileUploadIndicator } from './components/file-upload-indicator/file-upload-indicator';
import { ClipboardService } from './services/clipboard/clipboard';


@Component({
    selector: 'app-message-input',
    imports: [FormsModule, FileUploadIndicator],
    templateUrl: './message-input.html',
    styleUrl: './message-input.css',
    providers: [ClipboardService]
})
export class MessageInput {

    currentText: string = '';

    private clipboardService: ClipboardService = inject(ClipboardService);

    handleClipboardData(event: ClipboardEvent): void {
        event.preventDefault();

        const clipboardData = event.clipboardData;
        const clipboardItems = event.clipboardData?.items;

        if (clipboardItems !== undefined && clipboardData !== null) {
            this.clipboardService.process(clipboardData, clipboardItems);
            
        } else {
            console.log('data null: ', clipboardData);
        }

    }
}
