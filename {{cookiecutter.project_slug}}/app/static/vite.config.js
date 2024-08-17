// app/static/vite.config.js

import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

export default defineConfig({
  root: '.', // Use the current directory (app/static) as root
  base: '/',
  server: {
    open: false,
    host: true, // Expose server to network
    port: 5173, // Default port
  },
  build: {
    outDir: resolve(__dirname, 'dist'), // Output directory for build
    emptyOutDir: true,
    rollupOptions: {
      input: {
        styles: resolve(__dirname, 'css/styles.css'), // Entry point for your CSS
        main: resolve(__dirname, 'js/main.js'), // Entry point for your JS
      },
    },
  },
  css: {
    postcss: {
      plugins: [
        tailwindcss(resolve(__dirname, 'tailwind.config.js')), // Load your Tailwind config
        autoprefixer(),
      ],
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname), // Alias for root
    },
  },
});
