/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontSize: {
        'base': '18px',
      },
      colors: {
        'pending': '#9CA3AF',
        'cleaned': '#FDE047', 
        'approved': '#4ADE80',
        'rejected': '#F87171'
      }
    },
  },
  plugins: [],
}
