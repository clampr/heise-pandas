from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

pageviews = pd.read_csv('pageviews.csv', index_col='Date', parse_dates=['Date'])

# Mehrere Threads für schnellere Downloads
Daily.max_threads = 6

# Zeitliche Periode
start = datetime(2019, 12, 1)
end = datetime(2020, 11, 30)

# 50 Zufällige Wetterstationen in Deutschland
stations = Stations()
stations = stations.region('DE')
stations = stations.inventory('daily', (start, end))
stations = stations.fetch(limit=50, sample=True)

# Tageswerte laden
weather = Daily(stations, start, end)

# Daten monatlich aggregieren
weather = weather.aggregate('1MS', spatial=True).fetch()

# Titel des Diagramms
TITLE = 'Interesse an Klimaanlagen & Max. Temperaturen in Deutschland'

# Darstellung der Seitenaufrufe
ax = pageviews['Klimaanlage'].plot(color='tab:blue', title=TITLE)
ax.set_ylabel('Seitenaufrufe', color='tab:blue')

# Darstellung der Temperaturspitzen
ax2 = ax.twinx()
ax2.set_ylabel('Max. Temperatur (°C)', color='tab:red')
weather['tmax'].plot(ax=ax2, color='tab:red')

# Ausgabe des Diagramms
plt.show()
