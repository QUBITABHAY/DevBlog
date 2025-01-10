/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["basic_flask/templates/layout.html",
    "basic_flask/templates/about.html",
    "basic_flask/templates/home.html",
    "basic_flask/templates/register.html",
    "basic_flask/templates/login.html",
    "basic_flask/templates/account.html",
    "basic_flask/templates/create_post.html",
    "basic_flask/templates/post.html",
    "basic_flask/templates/user_post.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}