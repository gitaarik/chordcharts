from rest_framework import serializers
from .models import Chart, Section, Line, Measure, Chord


class ChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chart
        fields = (
            'id',
            'song',
            'short_description',
            'video_url',
            'lyrics_url'
        )


class SectionSerializer(serializers.ModelSerializer):

    key_id = serializers.SerializerMethodField('get_key_id')

    def get_key_id(self, obj):
        return obj.key.id

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `chart_id` field.
            attrs['chart_id'] = self.context['chart_id']

        return super().restore_object(attrs, instance)

    class Meta:
        model = Section
        fields = (
            'id',
            'key_id',
            'number',
            'alt_name',
            'time_signature',
            'show_sidebar'
        )


class LineSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `section_id` field.
            attrs['section_id'] = self.context['section_id']

        return super().restore_object(attrs, instance)

    class Meta:
        model = Line
        fields = ('id', 'number', 'letter')


class MeasureSerializer(serializers.ModelSerializer):

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `line_id` field.
            attrs['line_id'] = self.context['line_id']

        return super().restore_object(attrs, instance)

    class Meta:
        model = Measure
        fields = ('id', 'number', 'beat_schema')


class ChordSerializer(serializers.ModelSerializer):

    chord_type_id = serializers.PrimaryKeyRelatedField(source='chord_type')

    def restore_object(self, attrs, instance=None):

        if instance is None:
            # if `instance` is `None`, it means we're creating a new
            # object, so we set the `measure_id` field.
            attrs['measure_id'] = self.context['measure_id']

        return super().restore_object(attrs, instance)

    class Meta:
        model = Chord
        fields = (
            'id',
            'number',
            'beats',
            'chord_type_id',
            'chord_pitch',
            'alt_bass',
            'alt_bass_pitch',
            'rest'
        )
