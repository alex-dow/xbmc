define(['jquery'], function($) {
    return function(id, width, height) {

        this.palette = new Rickshaw.Color.Palette({ scheme: 'spectrum2001' });

        this.graph = new Rickshaw.Graph({
            element: document.querySelector('#' + id),
            width: width,
            height: height,
            renderer: 'area',
            min: 0,
            max: 100,
            series: new Rickshaw.Series.FixedDuration([{name: id}], undefined, {
                timeInterval: 250,
                maxDataPoints: width,
                timeBase: new Date().getTime() / 1000,
                color: this.palette.color()
            })
        });
        
    };
});
