from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters 
from ...models import Todo
from .serializers import TodoSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPagination

class TodoModelViewSet(viewsets.ModelViewSet):
    # ============= CRUD with one view based on ModelViewSet ============= # 
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = {'user__username':['exact','in']}
    search_fields = ['task','=user__username']
    ordering_fields = ['created_at']
    pagination_class = CustomPagination
    # ============= Listing the tasks which belong to existing user ============= # 
    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = Todo.objects.filter(user=user)
    #     return queryset

