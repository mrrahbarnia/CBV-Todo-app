from rest_framework import routers
from .views import TodoModelViewSet

# ============= Defaultrouter for generating all url's which belong to todo app ============= # 
router = routers.DefaultRouter()
router.register('todo',TodoModelViewSet,basename='todo')

urlpatterns = router.urls