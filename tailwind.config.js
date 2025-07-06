
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-gold': '#C0A062',
        'brand-blue': '#1E2A4A',
        'brand-light': '#F8F5F0',
        'brand-dark': '#12182B',
      }
    },
  },
  plugins: [],
}
