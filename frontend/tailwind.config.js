/** @type {import('tailwindcss').Config} */
module.exports = {
  content": [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme": {
    extend": {
      colors": {
        military: {
          'dark': '#0a0e1a',
        },
      },
    },
  },
  plugins": [require('daisyui')],
  daisyui": {
    themes": ['dark'],
  },
}
