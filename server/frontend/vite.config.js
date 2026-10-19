import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],base:'/static/',build:{outDir:'build'},server:{proxy:{'/djangoapp':'http://127.0.0.1:8000'}}});
