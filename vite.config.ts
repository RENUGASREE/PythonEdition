import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// DEPLOYMENT CONFIGURATION FOR VERCEL
// This configuration is optimized for Vercel deployment
// - Build output goes to dist/ directory
// - Proxy configuration for API calls to backend
// - Simplified chunk splitting to avoid build errors

export default defineConfig({
  plugins: [
    react(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
    },
  },
  root: path.resolve(import.meta.dirname, "client"),
  build: {
    outDir: path.resolve(import.meta.dirname, "dist"),
    emptyOutDir: true,
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          ui: ["@radix-ui/react-toast", "class-variance-authority", "@radix-ui/react-tooltip"],
          router: ["wouter"],
          query: ["@tanstack/react-query"],
        }
      }
    }
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
    proxy: {
      "/api": "http://localhost:8000",
      "/static": "http://localhost:8000",
    },
  },
  optimizeDeps: {
    include: ["@radix-ui/react-toast", "class-variance-authority", "@radix-ui/react-tooltip"],
  },
});
