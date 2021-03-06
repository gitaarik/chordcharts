var Model = require('../init/_model.js');


module.exports = Model.extend({

    url: (
        GLOBALS.api_root_url +
        'chart-song-name/' +
        GLOBALS.chart_data.id + '/'
    ),

    isNew: function() {
        return true;
    },

    toJSON: function() {

        return {
            song_name: this.get('song_name'),
        };

    }

});
