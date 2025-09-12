import { Component, ChangeDetectionStrategy, signal, EventEmitter, Output, input } from '@angular/core';
import { NgOptimizedImage } from '@angular/common';


@Component({
    selector: 'app-file-upload-item',
    imports: [NgOptimizedImage],
    templateUrl: './file-upload-item.html',
    styleUrl: './file-upload-item.css',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FileUploadItem {
    imageUrl = input<string>('');
  
    // Output event emitter to notify the parent component to delete this instance.
    // deleteComponent = signal<string>('');
    @Output() deleteComponent = new EventEmitter<void>();
}
