from django.urls import path

from . import views

app_name = 'financial_planner'
urlpatterns = [
    # ex: /financial_planner/
    path('', views.index, name='index'),
    # ex: /financial_planner/5/5
    path('<str:user_name>/<str:plan_name>/', views.plan, name='plan'),

    path('<str:user_name>/<int:plan_id>/addsource/', views.add_source, name='add_source'),

    path('<str:user_name>/<str:plan_id>/<int:source_id>/deletesource/', views.delete_source, name='delete_source'),
]