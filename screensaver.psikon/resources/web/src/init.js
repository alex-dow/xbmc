define(['jquery','underscore','backbone'], function($, _, Backbone) {

    var init = function() {
        this.foo = 'bar';
    };

    init.prototype.add = function(a,b) {
        return a + b;
    };

    return init;

});
