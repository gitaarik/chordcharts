define(
    [
        'collections/lines',
        'collections/measures',
        'models/chart',
        'views/section'
    ],
    function(
        Lines,
        Measures,
        Chart,
        SectionView
    ) {

        return Backbone.View.extend({

            className: 'chart',

            events: {
                'click .section-new': 'createNewSection'
            },

            createNewSection: function() {

                var last_section = this.model.get('sections').last();

                var new_section = last_section.copy({
                    number: last_section.get('number') + 1,
                    alt_name: '',
                });

                var new_line = new_section.get('lines').first().copy();
                var new_measure = new_line.get('measures').first().copy({
                    next_measure: null,
                    prev_measure: null
                });

                new_line.get('measures').reset([new_measure]);
                new_section.get('lines').reset([new_line]);

                this.model.get('sections').add(new_section);

                var sectionView = new SectionView({
                    model: new_section
                });

                sectionView.render().$el.insertBefore(
                    this.$el.find('.section-new')
                );

                new_section.saveRecursive();

            }

        });

    }
);