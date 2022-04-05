from datetime import date, timedelta
import smtplib


class Main:

    date_info = {}

    def __init__(self):
        self.curr_date = date.today()

    def accomplishment_date(self):
        self.date_info['start'] = Main.format_date(self.set_start_day())
        self.date_info['end'] = Main.format_date(date.today())
        self.date_info['next_start'] = Main.format_date(self.set_next_week_monday())
        self.date_info['next_end'] = Main.format_date(self.set_next_week_friday())

        return self.date_info

    # Get Monday Date
    def set_start_day(self):
        return self.curr_date - timedelta(days=4)

    def set_next_week_monday(self):
        return self.curr_date + timedelta(days=3)

    def set_next_week_friday(self):
        return self.curr_date + timedelta(days=7)

    @staticmethod
    def is_friday():
        if date.today().weekday() == 2:
            return True
        return False

    @staticmethod
    def format_date(date_to_format):
        return date_to_format.strftime("%B %d %Y")

if __name__ == "__main__":
    if Main().is_friday():
        main = Main()
        print(main.accomplishment_date())

