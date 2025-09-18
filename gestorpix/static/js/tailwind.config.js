module.exports = {
  darkMode: 'class', // habilita dark mode via classe
  content: [
    "./templates/**/*.html",   // vai procurar classes no HTML do Django
    "./static/js/**/*.js",     // e nos seus JS
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
