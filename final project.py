from datetime import datetime
import smtplib
from email.message import EmailMesaage
file = open("Records.txt", "a")


print("Welcome to CHA")
print("plese provide your information down below.")

name = input("what is your name? ")
age = input("How old are you? ")
email = input("What is your email? ")
file.write("This is The User's Information:\nName: " +name+ "\n""Age: " +age+ " Years old\n""Email: "+email+ "\n" )


while True:
   contact = input("have you recently made contact with an infected individual? (kindly answer in (yes,no) format\n ")
   if contact == 'yes':
        duration = input("how long has it been since your last contact? (days)\n ")
        if int(duration) < 4:
            print("quarantine yourself at home and perform social distancing procedures until it has been 4 or more days since the last contact with the infected person, and if you are suffering from symptoms of covid-19, check if the symptoms worsen then head to the nearest covid-19 test center.\n")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user has been adviced to: quarantine yourself at home and perform social distancing procedures until it has been 4 or more days since the last contact with the infected person, and if the symptoms worsen then head to the nearest covid-19 test center.\n")
            break
        elif int(duration) >= 10:
            print("You are no longer contagious. stay at home and perform social distancing procedres.")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user is no longer contagious.")
            file.write("the user has been adviced to: stay at home and perform social distancing procedres.")
            break
        elif int(duration) < 10:
            print("go to the nearest covid-19 test center.")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user has been adviced to: go to the nearest covid-19 test center.")
            break
        elif int(duration) == 4:
            print("Go to the nearest covid-19 test center.")
            file.write("the user has made contact with an infected person, "+str(duration)+ " days ago\n")
            file.write("the user has been advised to: go to the nearest covid-19 test center.")
            break

   elif contact == 'no':
           print("we will now ask you about major covid-19 symptoms (kindly answer in (yes\no) format .\n")
           major_symptom_1 = input(" do you have trouble breathing?\n ")
           if major_symptom_1 == "yes":
               print("Seek emergency medical care immediately.")
               file.write("the user is having trouble breathing\n")
               file.write("the user has been advised to: Seek emergency medical care immediately.")
               break
           major_symptom_2 = input("do you suffer from persistant pain or pressure in the chest?\n ")
           if major_symptom_2 == "yes":
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from:persistant pain or pressure in the chest\n ")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")

               break
           major_symptom_3 = input("do u suffer from new confusion?\n")
           if major_symptom_3 == "yes":
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from: new confusion\n")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")

               break
           major_symptom_4 = input("do you suffer from inability to wake or stay awake?\n")
           if major_symptom_4 =="yes":
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from: inability to wake or stay awake\n")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")

               break
           major_symptom_5 = input("do u suffer from bluish lips or face?\n ")
           if major_symptom_5 == "yes":
               print("Seek emergency medical care immediately.\n\n")
               file.write("the user is suffering from: bluish lips or face\n ")
               file.write("the user has been adviced to: Seek emergency medical care immediately.\n\n")

               break
           print("\n")
           print("we will now ask you about some common minor symptos of covid-19 (kindly answer in (yes,no) format.\n\n")
           symptoms = 0
           minor_symptom_1 = input("do you suffer from fever or chills?\n ")
           if minor_symptom_1 == "yes":
             file.write("the user is suffering from: fever or chills\n")
             symptoms = symptoms + 1
           minor_symptom_2 = input("do you suffer from a cough?\n ")
           if minor_symptom_2 == "yes" :
             file.write("the user is suffering from:  a cough\n")
             symptoms ==symptoms + 1
           minor_symptom_3 = input("do you suffer from shortness of breath or difficulty breathing ?\n ")
           if minor_symptom_3 == "yes":
               file.write("the user is suffering from: shortness of breath or difficulty breathing \n ")
               symptoms = symptoms + 1
           minor_symptom_4 = input("do you suffer from fatigue ?\n ")
           if minor_symptom_4 == "yes":
               file.write("the user is suffering from: fatigue \n")
               symptoms = symptoms + 1
           minor_symptom_5 = input("do you suffer from muscle or body aches?\n")
           if minor_symptom_5 == "yes":
               file.write("the user is suffering from: muscle or body aches\n")
               symptoms = symptoms + 1
           minor_symptom_6 = input("do you suffer from a headache?\n ")
           if minor_symptom_6 == "yes":
               file.write("the user is suffering from: a headache\n")
               symptoms = symptoms + 1
           minor_symptom_7 = input("do you suffer from new loss of taste or smell?\n")
           if minor_symptom_7 == "yes":
               file.write("the user is suffering from: new loss of taste or smell\n")
               symptoms = symptoms +1
           minor_symptom_8 = input("do you suffer from a sore throat?\n")
           if minor_symptom_8 == "yes":
               file.write("the user is suffering from: a sore throat\n")
               symptoms = symptoms +1
           minor_symptom_9 = input("do you suffer from congestion or runny nose?\n")
           if minor_symptom_9 == "yes":
               file.write("the user is suffering from: congestion or runny nose\n")
               symptoms = symptoms + 1
           minor_symptom_10 = input("do you suffer from nausea or vomittig or diarrhea?\n")
           if minor_symptom_10 == "yes":
               file.write("the user is suffering from: nausea or vomittig or diarrhea\n")
               symptoms = symptoms + 1
           if int(symptoms) == 0:
               print("stay home and perfom social distancing prcedures")
               file.write("the user suffers from no symptoms.\n")
               file.write("the user has been advised to : stay home and perfom social distancing prcedures")
           elif int(symptoms) >= 4 :
             print("head to the nearest covid-19 test center")
             file.write("the user has been advised to : head to the nearest covid-19 test center")
           elif int(symptoms) < 4 :
               print("quarantine yourself at home and perform social distancing procedures for 2-14 days and if the symptoms worsen then head to the nearest covid-19 test center.")
               file.write("the user has been advised to: quarantine yourself at home and perform social distancing procedures for 2-14 days and if the symptoms worsen then head to the nearest covid-19 test center.")

        s = smtplib.SMTP('localhost')
        msg = EmailMessage()
        msg.set_content(file.read())
        msg['Subject'] = ['this is you record']
        msg['From'] = momen.motaz@gmail.com
        msg['To'] = momen.motaz@gmail.com
        s.send_message(msg)
        s.quit()

           break


file.write("\n\n")
file.close()









