module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        bower: {
            install: {
            }
        },
        karma: {
          unit: {
                configFile: "test.conf.js"
            }
        }
    });

    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-karma');

    grunt.registerTask('prepare', ['bower:install']);
    grunt.registerTask('test', ['karma:unit']);

};
