define(['views/lineGraph', 'backbone','underscore','jquery'], function(LineGraph, Backbone, _, $) {

    return Backbone.View.extend({

        rows: {},

        initialize: function(options)
        {
            this.options = options;
            this.template = _.template($('#computer-row-template').html());
        },

        render: function(record) {
            if (!this.rows[record['hostname']]) {
                this.$el.append(this.template({hostname: record['hostname']}));
                this.rows[record['hostname']] = {
                    cpu_graph: new LineGraph(record['hostname'] + '-cpu-graph', 100, 50),
                    mem_graph: new LineGraph(record['hostname'] + '-mem-graph', 100, 50)
                };
            }

            this.rows[record['hostname']].cpu_graph.graph.series.addData({'cpu': record['cpu']});
            this.rows[record['hostname']].mem_graph.graph.series.addData({'mem': (record['mem_used'] / record['mem_total']) * 100});

            this.rows[record['hostname']].cpu_graph.graph.render();
            this.rows[record['hostname']].mem_graph.graph.render();
        }

    });

});
