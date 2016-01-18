'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var iconify = require('gulp-iconify');

gulp.task('build_icons', function() {
    iconify({
        src: './frontend/icons/*.svg',
        pngOutput: './static/volontulo/img/icons/png',
        cssDisabled: true,
        cssOutput: 'false',
        scssOutput: './frontend/scss/iconify',
        styleTemplate: './frontend/icons/template/icon_gen.scss.mustache',
        defaultWidth: '32px',
        defaultHeight: '32px',
        svgoOptions: {
            enabled: true,
            options: {
                plugins: [
                    { removeUnknownsAndDefaults: true },
                    { mergePaths: false }
                ]
            }
        }
    });
});

gulp.task('build_fonts', function() {
    gulp.src('./frontend/fonts/**/*')
        .pipe(gulp.dest('./static/volontulo/fonts/'));
});

gulp.task('build_img', function() {
    gulp.src('./frontend/img/**/*')
        .pipe(gulp.dest('./static/volontulo/img/'));
});

gulp.task('build_javascripts', function() {
    gulp.src('./frontend/javascripts/**/*.js')
        .pipe(gulp.dest('./static/volontulo/javascripts/'));
});

gulp.task('build_scss', function() {
    gulp.src('./frontend/scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/volontulo/css/'));
});

gulp.task('build:svg', ['build_icons'], function() {
});

gulp.task('build', ['build_fonts', 'build_img', 'build_javascripts', 'build_scss'], function() {
});

gulp.task('watch', ['build'], function() {
    gulp.watch('./frontend/**/*', ['build']);
    gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});
