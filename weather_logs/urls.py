"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'weather_logs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all Starts.
    path('states/', views.states, name='states'),
    # List of Weather Stations for a single state.
    path('states/<str:abbrev>/', views.state, name='state'),
    # Details for a Weather Station
    path('states/<str:abbrev>/<str:id>', views.station, name='station'),
    # Page for a specific year of station readings.
    path('states/<str:abbrev>/<str:id>/<int:year>', views.station_year, name='station_year'),
    # Page for editing an entry.
    #path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]