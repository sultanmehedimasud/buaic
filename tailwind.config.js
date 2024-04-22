/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      colors: {
        danger: {
          DEFAULT: '#e3342f',
        },
        success: {
          DEFAULT: '#38c172',
        },
        warning: {
          DEFAULT: '#f6993f',
        },},

      zIndex: {
        '1000': '1000',
        '2000': '2000',}
      },
  },
  plugins: [],
  purge: ['./templates/**/*.html', './static/js/**/*.js'],
}