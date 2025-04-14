from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer_class = self.parent.parent.__class__

        if isinstance(self.parent, serializers.ListSerializer):
            serializer_class = self.parent.parent.__class__
        else:
            serializer_class = self.parent.__class__
        return serializer_class(value, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    replies = RecursiveField(many=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request.user == obj.owner if request else False

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "post",
            "parent",
            "created_at",
            "updated_at",
            "content",
            "approval_status",
            "replies",
        ]


class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source="post.id")

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ["approval_status"]
