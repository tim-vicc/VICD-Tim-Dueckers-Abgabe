#importiort den Python Kalender und erstellt eine Klasse für den Kalender
import calendar
class workplaceCalendar:
    def __init__(self):
        self.Calendar = calendar.Calendar()

    def get_days(self, month, year):
        return self.Calendar.monthdatescalendar(year, month)
