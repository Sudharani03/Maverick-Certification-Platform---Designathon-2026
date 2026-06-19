/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#04134A',
          800: '#0A1E5C',
        },
        brand: {
          blue: '#154BC7',
          lightBlue: '#E3EBFE',
          orange: '#FEF6EB',
          green: '#57BC9A',
          teal: '#59BE9C',
        }
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
