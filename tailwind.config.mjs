/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        stage: {
          950: '#060b17', // deepest backdrop
          900: '#091224', // deep stage blue
          850: '#0d1830', // card container
          800: '#132347', // card highlight
          700: '#1e3566', // borders
        },
        theatre: {
          gold: '#f59e0b',
          'gold-light': '#fbbf24',
          'gold-dark': '#d97706',
          ruby: '#b91c1c',
          crimson: '#991b1b',
        }
      },
      fontFamily: {
        theatre: ['Cinzel', 'Playfair Display', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
};
