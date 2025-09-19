import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
    {
        path: '',
        renderMode: RenderMode.Prerender
    },
    {
        path: 'app',
        renderMode: RenderMode.Server
    },
    {
        path: 'app/content',
        renderMode: RenderMode.Server
    },
    {
        path: 'app/content/**',
        renderMode: RenderMode.Server
    }
];
