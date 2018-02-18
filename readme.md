#Vatsim Germany Python Beispiel

Wichtige Dateien:
1. `app/templates/base.html` Grund-Template von dem alle Seiten erben
2. `app/templates/bookings.html` Booking Seite
3. `app/routes/main.py` Definition der Views/Routen
4. `app/models.py` Definition der Tabellen in der Datenbank als Python objecte die vom ORM dann gemanaged werden

Installation:
1. Python installieren (3.x nicht 2.x)
2. `pip install -r requirements.txt` um die benötigten pakete zu installieren

Starten:
1. `python manage.py runserver`
2. `localhost:5000` im browser öffnen
3. http://sqlitebrowser.org/ installieren
4. `database.db` öffnen und dann einen `Member` anlegen
5. Links auf "Login" klicken und dann mit dem angelegten Member einloggen
6. Links auf "ATC Bookings" klicken 
