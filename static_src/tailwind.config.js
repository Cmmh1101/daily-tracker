module.exports = {
    content: [
      '../templates/**/*.html',
      '../../templates/**/*.html',
      '../../**/templates/**/*.html',
      '../../**/*.js',
      './static_src/src/**/*.js',
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
      require('@tailwindcss/line-clamp'),
      require('@tailwindcss/aspect-ratio'),
    ],
  }