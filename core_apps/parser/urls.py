from django.urls import path

from . import views


app_name = 'parser'


urlpatterns = [
    path('req_info/', views.req_info, name='req_info'),
    path('my_file/', views.my_file, name='my_file'),



    path('all/', views.view_index_all, name='index_all'),
    path('api/', views.view_json, name='api_json'),
    path('export_to_csv/', views.export_to_csv, name='export_to_csv'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('export_to_xlsx/', views.export_to_xlsx, name='export_to_xlsx'),
    path('comeback/', views.come_back_and_clear_dict, name='back'),
    path('form/', views.select_coins_from_form, name='form'),

    path('upload/', views.uploadFile, name="uploadFile"),  #загрузить файл в БД
    path('all_file/', views.all_file_view, name='all_file'), # архивные файлы
    path('pdf_file_view/<int:id>/', views.pdf_file_view, name='pdf_view'),  # просмотр файла PDF из БД

    path('', views.view_homepage, name='home')

]