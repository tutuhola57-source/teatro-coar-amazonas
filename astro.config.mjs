import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  output: 'static',
  site: 'https://tutuhola57-source.github.io',
  base: process.env.VERCEL ? '/' : '/teatro-coar-amazonas'
});
