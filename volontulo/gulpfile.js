'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');


gulp.task('build_fonts', function() {
    gulp.src('./frontend/fonts/**/*')
        .pipe(gulp.dest('./static/volontulo/fonts/'));
});

gulp.task('build_img', function() {
    gulp.src('./frontend/img/**/*')
        .pipe(gulp.dest('./static/volontulo/img/'));
});

gulp.task('build_scss', function() {
    gulp.src('./frontend/scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/volontulo/css/'));
});

gulp.task('build', ['build_fonts', 'build_img', 'build_scss'], function() {
});

gulp.task('watch', ['build'], function() {
    gulp.watch('./frontend/**/*', ['build']);
    gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});
