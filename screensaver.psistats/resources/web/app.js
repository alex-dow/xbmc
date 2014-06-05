require.config({
    
    baseUrl: '/src',
    
    paths: {
        jquery: '../lib/jquery/jquery',
        underscore: '../lib/underscore/underscore',
        backbone: '../lib/backbone/backbone',
        bootstrap: '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min'
    },

    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }

});


requirejs(['views/computers', 'jquery', 'bootstrap'], function(Computers, $) {

    var connection = new WebSocket('ws://localhost:9999');

    var computers = new Computers({
        'el': '#computers'
    });

    connection.onopen = function(event) {
        connection.send('hello');
    };

    connection.onmessage = function() {
        stats = JSON.parse(arguments[0].data);
        computers.render(stats); 
    };

});

/*
requirejs(['lineGraph', 'jquery'], function(LineGraph, $) {

    var connection = new WebSocket('ws://localhost:9999');
    connection.onopen = function(event) {
        connection.send('hello');
    };

    var buffer_cpu_data = {};
    var buffer_mem_data = {};
    var cpu_graphs = {};
    var mem_graphs = {};

    connection.onmessage = function() {
        stats = JSON.parse(arguments[0].data);

        if (!cpu_graphs[stats.hostname]) {

            var cpu_id = 'graph-' + stats.hostname + '-cpu';
            var mem_id = 'mem-' + stats.hostname + '-mem';

            $('#cpu-chart').append('<div id="' + cpu_id + '"></div>');
            $('#mem-chart').append('<div id="' + mem_id + '"></div>');
            cpu_graphs[stats.hostname] = new LineGraph(cpu_id, 100, 50);
            mem_graphs[stats.hostname] = new LineGraph(mem_id, 100, 50);
            render_legend = false;
        }

        buffer_cpu_data[stats.hostname] = stats.cpu;
        buffer_mem_data[stats.hostname] = (stats.mem_used / stats.mem_total) * 100;

        var cpu_data = {};
        cpu_data[stats.hostname] = buffer_cpu_data[stats.hostname];

        var mem_data = {};
        mem_data[stats.hostname] = buffer_mem_data[stats.hostname];

        cpu_graphs[stats.hostname].graph.series.addData(cpu_data);
        mem_graphs[stats.hostname].graph.series.addData(mem_data);
        
        cpu_graphs[stats.hostname].graph.render();
        mem_graphs[stats.hostname].graph.render();

    };

    connection.onerror = function (error) {
        console.log('WebSocket Error');
        console.log(arguments);
        connection.close();
    };
});
*/
