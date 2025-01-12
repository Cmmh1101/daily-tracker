module.exports = {
    content: [
        '../templates/**/*.html', // App-level templates
        '../../templates/**/*.html', // Project-level templates
        '../../**/templates/**/*.html', // Any templates in other apps
        '../../**/*.js', // JavaScript files
        '../../**/*.py', // Python files (optional, if you use Tailwind classes in strings)
        './templates/**/*.html', // Your Django app templates
        './static_src/src/**/*.{js,jsx,ts,tsx}', // JavaScript/TypeScript source files
        './static_src/src/**/*.css', // Tailwind directives in CSS
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
};