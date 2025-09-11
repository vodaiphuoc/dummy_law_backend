import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { Conversations } from './conversations/conversations';
import { MessageArea } from './message-area/message-area';
import { MessageInput } from './message-input/message-input';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Conversations, MessageArea, MessageInput],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontendv2');
}
