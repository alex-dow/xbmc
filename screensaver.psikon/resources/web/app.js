require.config({
    
    baseUrl: '/src',
    
    paths: {
        jquery: '../lib/jquery/jquery',
        underscore: '../lib/underscore/underscore',
        backbone: '../lib/backbone/backbone'
    }

});

requirejs(['init'], function() {

    var WIDTH = 250;
    var HEIGHT = 100;

    var render_legend = false;

    var mem_graph = new Rickshaw.Graph({
        element: document.querySelector("#mem-chart"),
        width: WIDTH,
        height: HEIGHT,
        renderer: 'line',
        min: 0,
        max: 100,
        series: new Rickshaw.Series.FixedDuration([{name:""}], undefined, {
            timeInterval: 250,
            maxDataPoints: WIDTH,
            timeBase: new Date().getTime() / 1000
        })
    });

    var cpu_graph = new Rickshaw.Graph( {
        element: document.querySelector("#cpu-chart"),
        width: WIDTH,
        height: HEIGHT,
        renderer: 'line',
        min: 0,
        max: 100,
        series: new Rickshaw.Series.FixedDuration([{name:""}], undefined, {
            timeInterval: 250,
            maxDataPoints: WIDTH,
            timeBase: new Date().getTime() / 1000
        })
    } );

    var cpu_legend = new Rickshaw.Graph.Legend({
        graph: cpu_graph,
        element: document.getElementById('cpu-legend')
    });

    var mem_legend = new Rickshaw.Graph.Legend({
        graph: mem_graph,
        element: document.getElementById('mem-legend')
    });


var cpu_highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: cpu_graph,
    legend: cpu_legend
});

var mem_highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: mem_graph,
    legend: mem_legend
});

var cpu_shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
    graph: cpu_graph,
    legend: cpu_legend
});

var mem_shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
    graph: mem_graph,
    legend: mem_legend
});

var cpu_hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: cpu_graph,
    formatter: function(series, x, y) {
        var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
        var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
        var content = swatch + series.name + ": " + parseInt(y) + '<br>' + date;
        return content;
    }
});

var mem_hoverDetail = new Rickshaw.Graph.HoverDetail({
    graph: mem_graph,
    formatter: function(series, x, y) {
        var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
        var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
        var content = swatch + series.name + ": " + parseInt(y) + '<br>' + date;
        return content;
    }
});
    var connection = new WebSocket('ws://localhost:9999');
    connection.onopen = function(event) {
        console.log('sending a message');
        connection.send('hello');
    };

    var cpu_data = {};
    var mem_data = {};

    connection.onmessage = function() {
        stats = JSON.parse(arguments[0].data);

        if (!cpu_data[stats.hostname]) {
            render_legend = true;
        }
        cpu_data[stats.hostname] = stats.cpu;
        mem_data[stats.hostname] = (stats.mem_used / stats.mem_total) * 100;

        cpu_graph.series.addData(cpu_data)
        mem_graph.series.addData(mem_data)

        cpu_graph.render();
        mem_graph.render();

        if (render_legend) {
            console.log(render_legend);
            cpu_legend.render();
            cpu_shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
                graph: cpu_graph,
                legend: cpu_legend
            });

            mem_legend.render();
            mem_shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
                graph: mem_graph,
                legend: mem_legend
            });

            render_legend = false;
        }
    };

    connection.onerror = function (error) {
        console.log('WebSocket Error');
        console.log(arguments);
        connection.close();
    };
});
