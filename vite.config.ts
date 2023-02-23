import { resolve } from "path"
import { defineConfig } from 'vite';
import sveltePreprocess from 'svelte-preprocess';

import { svelte } from '@sveltejs/vite-plugin-svelte';

import tailwindcss from "tailwindcss"
import autoprefixer from "autoprefixer"

export default defineConfig(({ mode }) => {
  return {
    root: "src",
    publicDir: "../public",
    server: { port: 8080 },
    build: {
      outDir: "../build",
    },
    resolve: {
      alias: {
        "~": resolve(__dirname, "src")
      },
    },
    plugins: [
      svelte({
        preprocess: sveltePreprocess({
          sourceMap: mode !== "build",
          postcss: {
            plugins: [
              tailwindcss(),
              autoprefixer(),
            ],
          },
        }),
      })
    ]
  }
})