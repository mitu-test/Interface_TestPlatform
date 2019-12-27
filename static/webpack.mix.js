var mix = require('laravel-mix');

mix.sass('./src/sass/styles.scss', './dist/css/styles.css')
    .copy('./src/js', './dist/js')
    .copy('./src/imgs', './dist/imgs');
