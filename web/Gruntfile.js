module.exports = function (grunt) {

    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt, {pattern: ['grunt-*', 'assemble-less']});


    // Configurable paths for the application
    var appConfig = {
        app: 'static/web/app',
        dist: 'dist'
    };
    // Define the configuration for all the tasks
    grunt.initConfig({
        // Project settings
        yeoman: appConfig,
        less: {
            options: {
                stripBanners: true, // Strip JavaScript banner comments from source files
                paths: '<%= yeoman.app %>/styles', // scan this directory for @import directives
                compress: false, // do not compress
                //report: 'gzip', // show a gzip file report
                sourceMapFilename: '<%= yeoman.app %>/styles/gen/styles.css.map', // Create a sourcemap to reference the .less files for easy style debugging
                imports: {
                    reference: ['variables.less', 'fonts.less', 'mixins.less', 'base.less', 'grid.less', 'defaults.less'], // Include references to these files for evalutating mixins/vars
                },
            },
            styles: {
                files: {
                    '<%= yeoman.app %>/styles/gen/main.css': ['<%= yeoman.app %>/styles/main.less'], // Create a main.css from main.less
                    '<%= yeoman.app %>/styles/gen/components.css': ['<%= yeoman.app %>/components/**/*.less'], // Combine all component files into a single components.css file
                }
            }
        },

        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1,
                keepBreaks: true
                },
            target: {
                files: {
                    '<%= yeoman.app %>/styles/gen/main.css': '<%= yeoman.app %>/styles/gen/main.css',
                    '<%= yeoman.app %>/styles/gen/components.css': '<%= yeoman.app %>/styles/gen/components.css'
                }
            }
        }
    });

    grunt.registerTask('styles', [
        'less',
        'cssmin'
    ]);
};