## Folder structure

src/app/
|-- app-feature                 <-- layout of main app after login with chat + add-on features
|   |-- app-feature.css
|   |-- app-feature.html
|   |-- app-feature.spec.ts
|   `-- app-feature.ts
|-- app.config.server.ts
|-- app.config.ts
|-- app.css
|-- app.html
|-- app.routes.server.ts
|-- app.routes.ts
|-- app.spec.ts
|-- app.ts
|-- chat                        <-- chat feature
|   |-- chat.css
|   |-- chat.html
|   |-- chat.spec.ts
|   |-- chat.ts
|   |-- conversations
|   |   |-- conversations.css
|   |   |-- conversations.html
|   |   |-- conversations.spec.ts
|   |   `-- conversations.ts
|   |-- message-area
|   |   |-- message-area.css
|   |   |-- message-area.html
|   |   |-- message-area.spec.ts
|   |   `-- message-area.ts
|   `-- message-input
|       |-- components
|       |   |-- add-files
|       |   |   |-- add-files.css
|       |   |   |-- add-files.html
|       |   |   |-- add-files.spec.ts
|       |   |   `-- add-files.ts
|       |   |-- file-upload-indicator
|       |   |   |-- file-upload-indicator.css
|       |   |   |-- file-upload-indicator.html
|       |   |   |-- file-upload-indicator.spec.ts
|       |   |   `-- file-upload-indicator.ts
|       |   `-- file-upload-item
|       |       |-- file-upload-item.css
|       |       |-- file-upload-item.html
|       |       |-- file-upload-item.spec.ts
|       |       `-- file-upload-item.ts
|       |-- message-input.css
|       |-- message-input.html
|       |-- message-input.spec.ts
|       |-- message-input.ts
|       `-- services
|           `-- clipboard
|               |-- clipboard.spec.ts
|               `-- clipboard.ts
|-- content-delivery            <-- add-on features are here
|   |-- content-delivery.css
|   |-- content-delivery.html
|   |-- content-delivery.spec.ts
|   `-- content-delivery.ts
|-- home                        <-- this is home page + login + register
|   |-- home.css
|   |-- home.html
|   |-- home.spec.ts
|   `-- home.ts
`-- shared
    `-- models
        `-- message-types.ts
