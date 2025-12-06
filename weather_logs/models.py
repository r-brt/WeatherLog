from django.db import models

# Create your models here.
class State(models.Model):
    """A State in the United States"""
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name
    
class Station(models.Model):
    """A Weather Monitoring Station"""
    station_id = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    elevation = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.station_id + ": "+ self.name
    
class DailyTemp(models.Model):
    """A Daily Temperature Reading at a Weather Station"""
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    date = models.DateField()
    temp_avg = models.IntegerField(null=True)
    temp_max = models.IntegerField(null=True)
    temp_min = models.IntegerField(null=True)

    @property
    def temp_median(self):
        if self.temp_min == None:
            return self.temp_max
        else:
            if self.temp_max == None:
                return self.temp_min
            else:
                return (self.temp_min + self.temp_max)/2.0


    def __str__(self):
        """Return a string representation of the model."""
        return self.date.strftime('%m/%d/%Y') + " " + self.station_id.station_id