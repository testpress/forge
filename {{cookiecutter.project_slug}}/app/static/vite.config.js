// app/static/vite.config.js

import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  root: '.', // Use the current directory (app/static) as root
  base: '/',
  server: {
    open: false,
    host: true, // Expose server to network
    port: 5173, // Default port
  },
  plugins: [
    tailwindcss(), // Tailwind v4: no PostCSS config needed, config lives in CSS
  ],
  build: {
    outDir: resolve(__dirname, 'dist'), // Output directory for build
    emptyOutDir: true,
    manifest: true, // Generate manifest.json for asset mapping
    rollupOptions: {
      input: {
        styles: resolve(__dirname, 'css/styles.css'), // Entry point for your CSS
        main: resolve(__dirname, 'js/main.js'), // Entry point for your JS
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname), // Alias for root
    },
  },
});
