from rest_framework import serializers
from ...models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # ============= Converting all data from Todo model into JSON format ============= # 
    user = serializers.CharField(source='user.username',read_only=True)
    task_snippet = serializers.ReadOnlyField(source='title_snippet')
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Todo
        fields = ['id','user','task','task_snippet','absolute_url','created_at','updated_at']
        read_only_fields = ['absolute_url']
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    def to_representation(self,instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('task_snippet',None)
            rep.pop('absolute_url',None)
        else:
            rep.pop('task',None)
        return rep
    def create(self,validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
        