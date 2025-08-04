/** @type {import('tailwindcss').Config} */
// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
      extend: {
        colors: {
          pastelPrimary: '#A3D5FF',
          pastelPrimaryHover: '#91C8F0',
          pastelGray: '#F3F4F6',
          pastelText: '#4A5568',
        }
      }
    },
  plugins: [],
}
