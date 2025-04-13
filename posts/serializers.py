from rest_framework import serializers
from posts.models import Post, PostTag
from likes.models import Like
import bleach


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    post_tags = serializers.StringRelatedField(many=True, read_only=True)
    tags = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    def sanitize_content(self, content):
        allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
            'p', 'strong', 'em', 'u', 's', 'span', 'br', 'ul', 'ol', 'li'
        ]
        allowed_attributes = {
            '*': ['style', 'class'],
            'span': ['style', 'class'],
            'p': ['class', 'style'],
            'li': ['class', 'data-list'],
        }
        return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)

    def create(self, validated_data):
        tags_str = validated_data.pop('tags', '')
        content = validated_data.get('content', '')
        if content:
            validated_data['content'] = self.sanitize_content(content)

        post = Post.objects.create(**validated_data)
        if tags_str:
            tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]
            for name in tag_names:
                tag_obj, created = PostTag.objects.get_or_create(name=name)
                post.post_tags.add(tag_obj)
        return post

    def update(self, instance, validated_data):
        tags_str = validated_data.pop('tags', None)

        if 'content' in validated_data:
            validated_data['content'] = self.sanitize_content(validated_data['content'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_str is not None:
            instance.post_tags.clear()
            tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]
            for name in tag_names:
                tag_obj, created = PostTag.objects.get_or_create(name=name)
                instance.post_tags.add(tag_obj)

        return instance

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'post_tags',
            'tags', 'like_id', 'likes_count', 'comments_count',
        ]
