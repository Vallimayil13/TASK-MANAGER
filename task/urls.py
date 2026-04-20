from django.urls import path
from task import views

urlpatterns = [
    path('', views.signup, name="signup"),
    path('login', views.user_login, name="login")  ,
    path('logout',views.user_logout, name="logout"), 
    path('task_list', views.task_list, name='task_list'),
    path('create_task', views.create_task, name='create_task'),
    path('update_task/<int:id>/', views.update_task, name='update_task'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('mark-overdue-done', views.mark_all_overdue_done, name='mark_all_overdue_done'),
]