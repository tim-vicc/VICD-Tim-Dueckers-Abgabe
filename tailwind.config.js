/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/**/forms.py"],
  theme: {
    extend: {},
  },
  safelist: ["alert-info", "alert-error"],
  plugins: [require("daisyui")],
};
