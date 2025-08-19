import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
import tailwindcssAnimate from 'tailwindcss-animate';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(process.cwd(), "src"),
    },
  },
  build: {
    rollupOptions: {
      onLog(level, log, handler) {
        if (
          log.code === 'INVALID_ANNOTATION' ||
          (typeof log.message === 'string' && log.message.includes('/*#__PURE__*/'))
        ) return;
        handler(level, log);
      },
      input: {
        main: path.resolve(process.cwd(), 'index.html')
      }
    }
  }
})
