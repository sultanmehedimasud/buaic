/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      zIndex: {
        '1000': '1000',
        '2000': '2000',
      },
    },
  },
  plugins: [],
  purge: ['./templates/**/*.html', './static/js/**/*.js'],
}

