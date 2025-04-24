from rest_framework import serializers
from posts.models import Post, PostTag
from likes.models import Like


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ["name"]


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    profile_tags = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    post_tags = PostTagSerializer(many=True, read_only=True)
    tags = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        if value.image.height > 4096:
            raise serializers.ValidationError("Image height larger than 4096px!")
        if value.image.width > 4096:
            raise serializers.ValidationError("Image width larger than 4096px!")
        return value

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None
    
    def get_profile_tags(self, obj):
        return [tag.name for tag in obj.owner.profile.profile_tags.all()]

    def create(self, validated_data):
        tags_str = validated_data.pop("tags", "")
        post = Post.objects.create(**validated_data)
        if tags_str:
            tag_names = [name.strip() for name in tags_str.split(",") if name.strip()]
            for name in tag_names:
                tag_obj, created = PostTag.objects.get_or_create(name=name)
                post.post_tags.add(tag_obj)
        return post

    def update(self, instance, validated_data):
        tags_str = validated_data.pop("tags", None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update tags if 'tags' provided
        if tags_str is not None:
            instance.post_tags.clear()
            tag_names = [name.strip() for name in tags_str.split(",") if name.strip()]
            for name in tag_names:
                tag_obj, created = PostTag.objects.get_or_create(name=name)
                instance.post_tags.add(tag_obj)

        return instance

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "profile_tags",
            "created_at",
            "updated_at",
            "title",
            "content",
            "image",
            "post_tags",
            "tags",
            "like_id",
            "likes_count",
            "comments_count",
        ]
