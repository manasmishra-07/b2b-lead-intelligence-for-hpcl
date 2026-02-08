/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'hpcl-blue': '#003DA5',
        'hpcl-red': '#E31E24',
        'hpcl-darkBlue': '#002A75',
        'hpcl-lightBlue': '#E0F2FE',
      },
    },
  },
  plugins: [],
}