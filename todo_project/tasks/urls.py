from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('tasks/<int:task_id>/',views.view_task,name='view_task'),
    path('tasks/new/',views.create_task,name='create_task'),
    path('tasks/<int:task_id>/edit/',views.edit_task,name='edit_task'),
    path('tasks/<int:task_id>/delete/',views.delete_task,name='delete_task'),
    path(
            'contact/',
            TemplateView.as_view(
                template_name='tasks/contact',
                extra_context={
                    'phone': '+1234567890',
                    'email': 'example@email.com'
                }
            ),
            name='contact'
        ),
]
