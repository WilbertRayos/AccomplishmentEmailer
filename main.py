from datetime import date, timedelta
import smtplib
from email.message import EmailMessage


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
    def is_lastweek_lastmonth():
        lastweek_month = (date.today() - timedelta(days=7)).month
        if lastweek_month is not date.today().month:
            return True
        return False

    @staticmethod
    def is_friday():
        if date.today().weekday() == 5:
            return True
        return False

    @staticmethod
    def format_date(date_to_format):
        return date_to_format.strftime("%B %d %Y")


class Filer:
    def file_reading(self):
        with open("accomplishment.txt", "r") as f:
            accomp = f.readlines()
            return accomp


class Messager(Main, Filer):
    USERNAME = "sender_email_address"
    PASSWORD = "sender_email_password"
    TO = "receiver_email"
    CC = ["receiver2_email", "receiver3_email"]

    def __init__(self):
        super(Messager, self).__init__()
        self.msg = EmailMessage()
        self.msg['Subject'] = f"Weekly Accomplishment Report - ({self.accomplishment_date()['start']} – {self.accomplishment_date()['end']})"
        self.msg['From'] = self.USERNAME
        self.msg['To'] = self.TO
        self.msg['Cc'] = self.CC

    def generate_message(self):
        body = ""
        curr_content = ""
        is_monthly = Main().is_lastweek_lastmonth()
        for line in self.file_reading():
            if line[0] is not "-":
                curr_content = line
                if line.strip() == "Monthly Accomplishment Report":
                    if is_monthly:
                        curr_content = line.strip()
                        body += "\n" + line
                else:
                    body += "\n" + line
            else:
                if curr_content == "":
                    continue
                else:
                    body += line

        return self.msg.set_content(body)

    def send_message(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.USERNAME, self.PASSWORD)
            smtp.send_message(self.msg)


if __name__ == "__main__":
    if Main().is_friday():
        messager = Messager()
        messager.generate_message()
        messager.send_message()

