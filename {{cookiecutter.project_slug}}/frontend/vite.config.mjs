// frontend/vite.config.mjs

import { defineConfig } from 'vite';
import { resolve } from 'path';
import { fileURLToPath } from 'url';
import tailwindcss from '@tailwindcss/vite';

const frontendDir = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  root: '.', // Use the current directory (frontend/) as root
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
    outDir: resolve(frontendDir, 'dist'), // Output directory for build
    emptyOutDir: true,
    manifest: true, // Generate manifest.json for asset mapping
    rollupOptions: {
      input: {
        styles: resolve(frontendDir, 'css/styles.css'), // Entry point for your CSS
        main: resolve(frontendDir, 'js/main.js'), // Entry point for your JS
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(frontendDir), // Alias for root
    },
  },
});
