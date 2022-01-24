from rest_framework.routers import DefaultRouter

# ImportViewSets
from .api import GenderViewSet, LoanViewSet

router = DefaultRouter()

router.register('new-loan', LoanViewSet, basename='new_loan')
router.register('genders', GenderViewSet, basename='genders')

urlpatterns = [
]

urlpatterns += router.urls
