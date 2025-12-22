# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models.generate_paper import PaperTopic, GeneratedPaper, PlagiarismCheck, UserProfile


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']


# class PaperTopicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaperTopic
#         fields = ['id', 'name', 'description', 'created_at']


# class GeneratedPaperSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     topic = PaperTopicSerializer(read_only=True)
#     topic_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
#     class Meta:
#         model = GeneratedPaper
#         fields = [
#             'id', 'user', 'title', 'topic', 'topic_id', 'requirements', 
#             'content', 'word_count', 'status', 'model_used', 'temperature', 
#             'max_tokens', 'created_at', 'updated_at', 'completed_at'
#         ]
#         read_only_fields = ['user', 'content', 'word_count', 'status', 'completed_at']
    
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)


# class PlagiarismCheckSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     paper = GeneratedPaperSerializer(read_only=True)
#     paper_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
#     class Meta:
#         model = PlagiarismCheck
#         fields = [
#             'id', 'user', 'paper', 'paper_id', 'title', 'content', 
#             'similarity_percentage', 'report_url', 'report_data', 'status', 
#             'api_used', 'created_at', 'updated_at', 'completed_at'
#         ]
#         read_only_fields = [
#             'user', 'similarity_percentage', 'report_url', 'report_data', 
#             'status', 'api_used', 'completed_at'
#         ]
    
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)


# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
    
#     class Meta:
#         model = UserProfile
#         fields = [
#             'id', 'user', 'avatar', 'bio', 'papers_generated', 
#             'plagiarism_checks', 'preferred_model', 'default_temperature',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['papers_generated', 'plagiarism_checks']


# # 用于创建论文的简化序列化器
# class CreatePaperSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=500)
#     topic_id = serializers.IntegerField(required=False, allow_null=True)
#     requirements = serializers.CharField()
#     model_used = serializers.CharField(max_length=100, default='gpt-3.5-turbo')
#     temperature = serializers.FloatField(default=0.7, min_value=0.0, max_value=2.0)
#     max_tokens = serializers.IntegerField(default=4000, min_value=100, max_value=8000)


# # 用于创建查重检测的简化序列化器
# class CreatePlagiarismCheckSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=500)
#     content = serializers.CharField()
#     paper_id = serializers.IntegerField(required=False, allow_null=True) 