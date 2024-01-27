/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors:{
        textColor: '#EBEBEA',
        headerColor: "#021027",
        primary: "#02183C",
        secondary: "#CC5F00"
      }
    },
  },
  plugins: [],
}

