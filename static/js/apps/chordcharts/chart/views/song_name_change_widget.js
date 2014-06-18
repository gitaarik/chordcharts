define(
    [],
    function() {

        return Backbone.View.extend({

            initialize: function() {
                this.listenTo(this.model, 'change', this.render);
            },

            events: {
                'click h1': 'toggle'
            },

            toggle: function() {
                this.model.set('visible', !this.model.get('visible'));
            },

            render: function() {

                if (this.model.get('visible')) {
                    this.$el.find('.song-name-change').show();
                    this.focusTextField();
                } else {
                    this.$el.find('.song-name-change').hide();
                }

            },

            focusTextField: function() {

                var song_name_input = this.$el.find('.song-name-input');
                console.log(song_name_input);

                // set focus on text field
                song_name_input.focus();

                // make sure the cursor is at the end
                var orig_value = song_name_input.val();
                song_name_input.val('');
                song_name_input.val(orig_value);

            }

        });

    }
);
