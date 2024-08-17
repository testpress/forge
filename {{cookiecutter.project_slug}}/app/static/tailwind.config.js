/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.{html,js}"{% if cookiecutter.use_preline == 'y' %},
    'node_modules/preline/dist/*.js',{% endif %}
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'){% if cookiecutter.use_preline == 'y' %},
    require('preline/plugin'),{% endif %}
  ],
}
