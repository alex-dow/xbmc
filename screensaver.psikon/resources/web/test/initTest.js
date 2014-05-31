define(['init'], function(init) {
    describe('init', function() {
        it('adds', function() {
            var i = new init();
            expect(i.add(1,1)).toEqual(2);
        });
    });
});
