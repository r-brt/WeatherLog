from django.shortcuts import render
import numpy as np
import datetime

from .models import State, Station, DailyTemp

# Create your views here.
def index(request):
    """The home page for Weather Log."""
    return render(request, 'weather_logs/index.html')

def states(request):
    """Show all states."""
    states = State.objects.order_by('name')
    states_inactive = []

    for state in states:
        stations = state.station_set
        if(stations.count() == 0):
            states_inactive.append(state)
            states = states.exclude(id=state.id)

    context = {'states': states, 'states_inactive':states_inactive}
    return render(request, 'weather_logs/states.html', context)

def state(request, abbrev):
    """Show a single state and all its Weather Stations."""
    state = State.objects.get(abbreviation=abbrev)
    stations = state.station_set.order_by('name')
    stations_inactive = []
    # do not list any stations that do not have any readings yet
    for station in stations:
        dailies = station.dailytemp_set
        dailies = dailies.exclude(temp_min=None, temp_max=None)
        if(dailies.count() == 0):
            stations_inactive.append(station)
            stations = stations.exclude(id=station.id)
    context = {'state': state, 'stations': stations, 'stations_inactive': stations_inactive}
    return render(request, 'weather_logs/state.html', context)

def station(request, abbrev, id):
    """Show details for a single Weather Station for most recent year."""
    station = Station.objects.get(station_id=id)
    dailies = station.dailytemp_set.order_by('date')
    year = dailies.latest("date").date.year
    
    return station_year(request, abbrev, id, year)

def station_year(request, abbrev, id, year):
    """Show details for a single Weather Station for a given year."""
    station = Station.objects.get(station_id=id)
    dailies = station.dailytemp_set.order_by('date')
    dailies = dailies.exclude(temp_min=None, temp_max=None)
    total = dailies.count()
    years = [x.year for x in dailies.dates('date','year')]
    dailies = dailies.filter(date__year=year)
    total_year = dailies.count()
    state = station.state

    # calculate monthly averages for current year
    months_labels = []
    monthly_minmax = []

    months = [x.month for x in dailies.dates('date','month')]
    for x in range (1,13):
        monthlies = dailies.filter(date__month=x)
        min_list = monthlies.values_list('temp_min', flat=True).exclude(temp_min__isnull=True)
        max_list = monthlies.values_list('temp_max', flat=True).exclude(temp_max__isnull=True)
        if(min_list.count() == 0):
            min_med = " ? "
        else:
            min_med = f"{np.mean(min_list):.1f}"
            
        if(max_list.count() == 0):
            max_med = " ? "
        else:
            max_med = f"{np.mean(max_list):.1f}"
        #month = monthlies.filter(date__month=x).first().date.strftime('%B')
        month = datetime.datetime(2025, x, 1).strftime('%B')
        months_labels.append(month)
        monthly_minmax.append((min_med,max_med))        






    context = {'station': station, 'dailies': dailies, 'total': total,
               'total_year': total_year, 'year':year, 'years':years, 
               'abbrev':abbrev, 'state':state, 'months_labels':months_labels, 'monthly_minmax':monthly_minmax}
    return render(request, 'weather_logs/station_year.html', context)