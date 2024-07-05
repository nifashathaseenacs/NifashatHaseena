import mysql.connector
import pandas as pd
import smtplib
import random
import csv
import datetime

class MLA_Election:
    def __init__(self):
        self.candidates = {1: "Muthulakshmi", 2: "Kamalakannan", 3: "Sethupathi", 4: "Thanapal"}
        self.vote_count = {i: 0 for i in self.candidates.keys()}
        self.conn = mysql.connector.connect(
            host='localhost',
            database='tn_election',
            user='root',
            password='12345'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS voting (email VARCHAR(255), candidate INT)")
        self.conn.commit()

    def email(self):
        try:
            enter_email = input("Enter your mail id: ")
            otp = random.randint(00000, 99999)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("nifashathaseena@gmail.com", "hwxx hoya balj tmsp")
            msg = f"Your OTP is {otp}"
            s.sendmail("your-email@gmail.com", enter_email, msg)
            s.quit()
            otp_input = int(input("Enter the OTP: "))
            if otp == otp_input:
                return enter_email
            else:
                print("Invalid OTP")
                return False
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
            return False

    def voting(self, email):
        while True:
            x = datetime.datetime.now()
            print("\nElection Menu:")
            print("------------")
            print("1. Muthulaakshmi")
            print("2. Kamalakannan")
            print("3. sethupathi")
            print("4. Thanapal")
            print("0. Exit")
            vote = int(input("Enter your vote: "))
            if vote == 0:
                self.result()
                print("Closing the election system. Goodbye!")
                break
            elif vote in self.candidates.keys():
                print(f"Thank you for your vote! at {x}")
                self.vote_count[vote] += 1
                self.cursor.execute("INSERT INTO voting (email, candidate) VALUES (%s, %s)", (email, vote))
                self.conn.commit()
                print("Vote recorded successfully!")
                self.email()
            else:
                print("Oh oh! There is no candidate in that number")

    def result(self):
        with open('vote.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["candidate", "votes"])
            for i, j in self.vote_count.items():
                writer.writerow([self.candidates[i], j])
        for i, j in self.vote_count.items():
            print(f"{self.candidates[i]}: {j}")
        max_votes = max(self.vote_count.values())
        winners = [i for i, j in self.vote_count.items() if j == max_votes]
        if len(winners) == 1:
            print(f"The winner is {self.candidates[winners[0]]}")
        else:
            print("It's a tie between:")
            for winner in winners:
                print(self.candidates[winner])

mla_election = MLA_Election()
email = mla_election.email()
if email:
    mla_election.voting(email)