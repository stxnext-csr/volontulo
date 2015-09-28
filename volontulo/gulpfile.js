'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');

gulp.task('build', function() {
    gulp.src('./frontend/**/*')
        .pipe(gulp.dest('./static/volontulo/'));
});

gulp.task('watch', ['build'], function() {
    gulp.watch('./frontend/**/*', ['build']);
    gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});
