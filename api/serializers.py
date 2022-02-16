from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# Takes Project model and converts it into a json object
class ProjectSerializer(serializers.ModelSerializer):
    # Overriding what owner key returns in the JSON response
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)

    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    # Needs to start with get_
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data