import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class KalaCinemas:
    def __init__(self):
        self.movies = ['Aranmanai4', 'Billa', 'Gilli']
        self.classes = {"first class": 200, "second class": 250}
        self.gst_rate = 1.5

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="Maari_Build"
        )
        self.cursor = self.db.cursor()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS Maari_Build")
        self.db.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Films (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(255),
                email VARCHAR(255),
                total DECIMAL(10, 2)
            )
        """)
        self.db.commit()

    def display_movies(self):
        print("KalaCinemas")
        print("Available movies:")
        for movie in self.movies:
            print(movie)

    def get_movie_details(self):
        Enter_movie = input("Enter movie name: ")
        if Enter_movie in self.movies:
            print("Movie is available")
            return Enter_movie
        else:
            print("Movie is not available")
            return None

    def get_class_details(self):
        enter_class = input("Enter your class: ")
        if enter_class in self.classes:
            print("Your ticket price is", self.classes[enter_class])
            return enter_class
        else:
            print("Class is not available")
            return None

    def calculate_total(self, enter_class, how_many):
        base_total = self.classes[enter_class] * int(how_many)
        gst_amount = base_total * self.gst_rate
        total = base_total + gst_amount
        print(f"Your total price is, { total:.2f}")
        return total,gst_amount

    def make_payment(self, cm, pay):
        if cm == "on hand" and pay == "paid":
            print("Your ticket is booked")
            return True
        elif cm == "online" and pay == "paid":
            print("Your ticket is booked")
            return True
        else:
            print("Your ticket is not booked")
            return False

    def send_email(self, bill, total,gst_amount):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("nifashathaseena@gmail.com", "hwxx hoya balj tmsp")
            msg = MIMEMultipart()
            msg['From']="nifashathaseena@gmail.com"
            msg['To']=bill
            msg['Subject']="Your Ticket Details"
            body=(
                f"Single Ticket amount is:{total - gst_amount:.2f}\n\n"
                f"Ticket amount with GST amount:{gst_amount:.2f}\n\n"
                f"Total price of your ticket is:{total:.2f}\n\n"
            )
            msg.attach(MIMEText(body,'plain'))

            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print("Error sending email:", e)
        except Exception as e:
            print("An error occurred:", e)

    def book_ticket(self):
        self.display_movies()
        Enter_movie = self.get_movie_details()
        if Enter_movie:
            enter_class = self.get_class_details()
            if enter_class:
                how_many = int(input("How many tickets: "))
                total,gst_amount = self.calculate_total(enter_class, how_many)
                cm = input("Is cash pay in online or on hand: ")
                pay = input("paid/unpaid? ")
                if self.make_payment(cm, pay):
                    bill = input("Enter your mail for bill: ")
                    self.send_email(bill, total,gst_amount)
                    self.cursor.execute("""INSERT INTO Films (movie_name, email, total)VALUES (%s, %s, %s)""", (Enter_movie, bill, total))
                    self.db.commit()
                    print("Ticket booked successfully!")

if __name__ == "__main__":
    kala_cinemas = KalaCinemas()
    kala_cinemas.create_database()
    kala_cinemas.create_table()
    while True:
        command = input("Type 'book' to book a ticket or 'exit' to exit: ")
        if command.lower() == 'exit':
            break
        elif command.lower() == 'book':
            kala_cinemas.book_ticket()
        else:
            print("Invalid command. Please try again.")