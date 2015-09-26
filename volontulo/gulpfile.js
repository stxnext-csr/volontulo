'use strict';

var gulp = require('gulp');

gulp.task('build', function() {
    gulp.src('frontend/*')
        .pipe(gulp.dest('static/volontulo/'));
});
