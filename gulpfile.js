/*global -$ */
'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();

var browserify = require('browserify');
var browserSync = require('browser-sync');
var reactify = require('reactify');
var source = require('vinyl-source-stream');
var watchify = require('watchify');

var reload = browserSync.reload;

var path = {
  HTML: 'frontend/*.html',
  MAIN_LESS: 'frontend/styles/main.less',
  MAIN_JS: './frontend/scripts/main.js',
  JS: 'frontend/scripts/**/*.js',
  FONTS: 'frontend/fonts/**/*',
  IMAGES: 'frontend/images/**/*',
  MINIFIED_OUT: 'main.min.js',
  DEST_BUILD_JS: '.tmp/scripts',
  DEST_BUILD_CSS: '.tmp/styles',
  DEST_FONTS: '.tmp/fonts/**/*',
};
path.WATCHING = [
    path.HTML,
    path.MAIN_LESS,
    path.JS,
    path.DEST_BUILD_JS,
    path.IMAGES,
    path.DEST_FONTS
];


gulp.task('templates', function () {
  browserify(path.MAIN_JS)
    .transform(reactify)
    .bundle()
    .pipe(source('main.js'))
    .pipe(gulp.dest(path.DEST_BUILD_JS));
});


gulp.task('styles', function () {
  return gulp.src(path.MAIN_LESS)
    .pipe($.sourcemaps.init())
    .pipe($.less({
      paths: ['.']
    }))
    .pipe($.postcss([
      require('autoprefixer-core')({browsers: ['last 1 version']})
    ]))
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest(path.DEST_BUILD_CSS))
    .pipe(reload({stream: true}));
});


gulp.task('jshint', function () {
  return gulp.src(path.JS)
    .pipe(reload({stream: true, once: true}))
    .pipe($.jshint())
    .pipe($.jshint.reporter('jshint-stylish'))
    .pipe($.if(!browserSync.active, $.jshint.reporter('fail')));
});


gulp.task('html', ['styles', 'templates'], function () {
  var assets = $.useref.assets({searchPath: ['.tmp', 'frontend', '.']});

  return gulp.src(path.HTML)
    .pipe(assets)
    .pipe($.if('*.js', $.uglify()))
    .pipe($.if('*.css', $.csso()))
    .pipe(assets.restore())
    .pipe($.useref())
    .pipe($.if('*.html', $.minifyHtml({conditionals: true, loose: true})))
    .pipe(gulp.dest('dist'));
});


gulp.task('images', function () {
  return gulp.src('frontend/images/*')
    .pipe($.cache($.imagemin({
      progressive: true,
      interlaced: true,
      // don't remove IDs from SVGs, they are often used
      // as hooks for embedding and styling
      svgoPlugins: [{cleanupIDs: false}]
    })))
    .pipe(gulp.dest('dist/images'));
});

gulp.task('fonts', function () {
  return gulp.src(require('main-bower-files')({
    filter: '**/*.{eot,svg,ttf,woff,woff2}'
  }).concat('frontend/fonts/**/*'))
    .pipe(gulp.dest('.tmp/fonts'))
    .pipe(gulp.dest('dist/fonts'));
});


gulp.task('extras', function () {
  return gulp.src([
    'frontend/*.*',
    '!frontend/*.html'
  ], {
    dot: true
  }).pipe(gulp.dest('dist'));
});


gulp.task('clean', require('del').bind(null, ['.tmp', 'dist']));


gulp.task('serve', ['styles', 'templates', 'fonts'], function () {
  browserSync({
    notify: false,
    port: 9000,
    server: {
      baseDir: ['.tmp', 'frontend'],
      routes: {
        '/bower_components': 'bower_components'
      }
    }
  });
  gulp.watch([
    'frontend/*.html',
    'frontend/scripts/*.js',
    '.tmp/scripts/*.js',
    'frontend/images/**/*',
    '.tmp/fonts/**/*'
  ]).on('change', reload);
  gulp.watch('frontend/styles/**/*.less', ['styles']);
  gulp.watch(path.JS, ['templates']);
  gulp.watch(path.FONTS, ['fonts']);
  gulp.watch('bower.json', ['wiredep', 'fonts']);
});


gulp.task('wiredep', function () {
  var wiredep = require('wiredep').stream;

  gulp.src('frontend/styles/*.less')
    .pipe(wiredep({
      ignorePath: /^(\.\.\/)+/
    }))
    .pipe(gulp.dest('frontend/styles'));

  gulp.src('frontend/*.html')
    .pipe(wiredep({
      ignorePath: /^(\.\.\/)*\.\./
    }))
    .pipe(gulp.dest('frontend'));
});


gulp.task('build', ['jshint', 'html', 'images', 'fonts', 'extras'], function () {
  return gulp.src('dist/**/*').pipe($.size({title: 'build', gzip: true}));
});


gulp.task('default', ['clean'], function () {
  gulp.start('build');
});
