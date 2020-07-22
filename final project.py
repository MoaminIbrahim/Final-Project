from datetime import datetime
import smtplib
from email.message import EmailMessage
file = open("Records.txt", "a")


print("Welcome to CHA")
print("plese provide your information down below.")

name = input("what is your name? ")
age = input("How old are you? ")
email = input("What is your email? ")
file.write("This is The User's Information:\nName: " +name+ "\n""Age: " +age+ " Years old\n""Email: "+email+ "\n" )


major_symptoms = []

minor_symptoms = []

advise = []

major_symptoms_1_n = "trouble breathing"
major_symptoms_2_n = "persistant pain or pressure in the chest"
major_symptoms_3_n = "new confusion"
major_symptoms_4_n = "inability to wake or stay awake"
major_symptoms_5_n = "bluish lips or face"

minor_symptoms_1_n = "fever or chills"
minor_symptoms_2_n = "a cough"
minor_symptoms_3_n = "shortness of breath or difficulty breathing"
minor_symptoms_4_n = "fatigue"
minor_symptoms_5_n = "muscle or body aches"
minor_symptoms_6_n = "a headache"
minor_symptoms_7_n = "new loss of taste or smell"
minor_symptoms_8_n = "a sore throat"
minor_symptoms_9_n = "congestion or runny nose"
minor_symptoms_10_n = "nausea or vomittig or diarrhea"
while True:
   contact = input("have you recently made contact with an infected individual? (kindly answer in (yes,no) format\n ")
   if contact == 'yes':

        duration = input("how long has it been since your last contact? (days)\n ")

        if int(duration) < 4:
            advise.append("quarantine yourself at home and perform social distancing procedures until it has been 4 or more days since the last contact with the infected person, and if you are suffering from symptoms of covid-19, check if the symptoms worsen then head to the nearest covid-19 test center.\n")

            print("quarantine yourself at home and perform social distancing procedures until it has been 4 or more days since the last contact with the infected person, and if you are suffering from symptoms of covid-19, check if the symptoms worsen then head to the nearest covid-19 test center.\n")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user has been adviced to: quarantine yourself at home and perform social distancing procedures until it has been 4 or more days since the last contact with the infected person, and if the symptoms worsen then head to the nearest covid-19 test center.\n")
            break


        elif int(duration) >= 10:
            advise.append("You are no longer contagious. stay at home and perform social distancing procedres.")
            print("You are no longer contagious. stay at home and perform social distancing procedres.")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user is no longer contagious.")
            file.write("the user has been adviced to: stay at home and perform social distancing procedres.")
            break
        elif int(duration) < 10:
            advise.append("go to the nearest covid-19 test center.")
            print("go to the nearest covid-19 test center.")
            file.write("the user has made contact with an infected person, " +str(duration)+" days ago.\n")
            file.write("the user has been adviced to: go to the nearest covid-19 test center.")
            break
        elif int(duration) == 4:
            advise.append("Go to the nearest covid-19 test center.")
            print("Go to the nearest covid-19 test center.")
            file.write("the user has made contact with an infected person, "+str(duration)+ " days ago\n")
            file.write("the user has been advised to: go to the nearest covid-19 test center.")
            break

   elif contact == 'no':
           print("we will now ask you about major covid-19 symptoms (kindly answer in (yes\no) format .\n")
           duration = str(0)
           major_symptom_1 = input(" do you have trouble breathing?\n ")
           if major_symptom_1 == "yes":
               advise.append("Seek emergency medical care immediately.")
               print("Seek emergency medical care immediately.")
               file.write("the user is having trouble breathing\n")
               file.write("the user has been advised to: Seek emergency medical care immediately.")
               major_symptoms.append(major_symptoms_1_n)
               break
           major_symptom_2 = input("do you suffer from persistant pain or pressure in the chest?\n ")
           if major_symptom_2 == "yes":
               advise.append("Seek emergency medical care immediately.")
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from: persistant pain or pressure in the chest\n ")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")
               major_symptoms.append(major_symptoms_2_n)

               break
           major_symptom_3 = input("do u suffer from new confusion?\n")
           if major_symptom_3 == "yes":
               advise.append("Seek emergency medical care immediately.")
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from: new confusion\n")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")
               major_symptoms.append(major_symptoms_3_n)

               break
           major_symptom_4 = input("do you suffer from inability to wake or stay awake?\n")
           if major_symptom_4 =="yes":
               advise.append("Seek emergency medical care immediately.")
               print("Seek emergency medical care immediately.")
               file.write("the user is suffering from: inability to wake or stay awake\n")
               file.write("the user has been adviced to: Seek emergency medical care immediately.")
               major_symptoms.append(major_symptoms_4_n)

               break
           major_symptom_5 = input("do u suffer from bluish lips or face?\n ")
           if major_symptom_5 == "yes":
               advise.append("Seek emergency medical care immediately.")
               print("Seek emergency medical care immediately.\n\n")
               file.write("the user is suffering from: bluish lips or face\n ")
               file.write("the user has been adviced to: Seek emergency medical care immediately.\n\n")
               major_symptoms.append(major_symptoms_5_n)

               break
           print("\n")
           print("we will now ask you about some common minor symptos of covid-19 (kindly answer in (yes,no) format.\n\n")
           symptoms = 0
           minor_symptom_1 = input("do you suffer from fever or chills?\n ")
           if minor_symptom_1 == "yes":
             file.write("the user is suffering from: fever or chills\n")
             minor_symptoms.append(minor_symptoms_1_n)
             symptoms = symptoms + 1
           minor_symptom_2 = input("do you suffer from a cough?\n ")
           if minor_symptom_2 == "yes" :
             file.write("the user is suffering from:  a cough\n")
             minor_symptoms.append(minor_symptoms_2_n)
             symptoms ==symptoms + 1
           minor_symptom_3 = input("do you suffer from shortness of breath or difficulty breathing ?\n ")
           if minor_symptom_3 == "yes":
               file.write("the user is suffering from: shortness of breath or difficulty breathing \n ")
               minor_symptoms.append(minor_symptoms_3_n)
               symptoms = symptoms + 1
           minor_symptom_4 = input("do you suffer from fatigue ?\n ")
           if minor_symptom_4 == "yes":
               file.write("the user is suffering from: fatigue \n")
               minor_symptoms.append(minor_symptoms_4_n)
               symptoms = symptoms + 1
           minor_symptom_5 = input("do you suffer from muscle or body aches?\n")
           if minor_symptom_5 == "yes":
               file.write("the user is suffering from: muscle or body aches\n")
               minor_symptoms.append(minor_symptoms_5_n)
               symptoms = symptoms + 1
           minor_symptom_6 = input("do you suffer from a headache?\n ")
           if minor_symptom_6 == "yes":
               file.write("the user is suffering from: a headache\n")
               minor_symptoms.append(minor_symptoms_6_n)
               symptoms = symptoms + 1
           minor_symptom_7 = input("do you suffer from new loss of taste or smell?\n")
           if minor_symptom_7 == "yes":
               file.write("the user is suffering from: new loss of taste or smell\n")
               minor_symptoms.append(minor_symptoms_7_n)
               symptoms = symptoms +1
           minor_symptom_8 = input("do you suffer from a sore throat?\n")
           if minor_symptom_8 == "yes":
               file.write("the user is suffering from: a sore throat\n")
               minor_symptoms.append(minor_symptoms_8_n)
               symptoms = symptoms +1
           minor_symptom_9 = input("do you suffer from congestion or runny nose?\n")
           if minor_symptom_9 == "yes":
               file.write("the user is suffering from: congestion or runny nose\n")
               minor_symptoms.append(minor_symptoms_9_n)
               symptoms = symptoms + 1
           minor_symptom_10 = input("do you suffer from nausea or vomittig or diarrhea?\n")
           if minor_symptom_10 == "yes":
               file.write("the user is suffering from: nausea or vomittig or diarrhea\n")
               minor_symptoms.append(minor_symptoms_10_n)
               symptoms = symptoms + 1
           if int(symptoms) == 0:
               advise.append("stay home and perfom social distancing prcedures")
               print("stay home and perfom social distancing prcedures")
               file.write("the user suffers from no symptoms.\n")
               file.write("the user has been advised to : stay home and perfom social distancing prcedures")
           elif int(symptoms) >= 4 :
             advise.append("head to the nearest covid-19 test center")
             print("head to the nearest covid-19 test center")
             file.write("the user has been advised to : head to the nearest covid-19 test center")
           elif int(symptoms) < 4 :
               advise.append("head to the nearest covid-19 test center")
               print("quarantine yourself at home and perform social distancing procedures for 2-14 days and if the symptoms worsen then head to the nearest covid-19 test center.")
               file.write("the user has been advised to: quarantine yourself at home and perform social distancing procedures for 2-14 days and if the symptoms worsen then head to the nearest covid-19 test center.")



           break
s = smtplib.SMTP('relay.andrew.cmu.edu')
msg = EmailMessage()
msg.set_content("This is The User's Information:\n Name: " +name+"\n" "Age: " +age+ " Years old\n"" Email: " +email+ "\n"  "have you made contact with an infected indvidual? "+contact+ "\n""contact has been made " +duration+" days ago\n" "your symptoms are: "+str(major_symptoms + minor_symptoms)+ "\n""you have been advised to: " +str(advise))
msg['Subject'] = "This is your CHA record"
msg['From'] = "CHA.final.project@gmail.com"
msg['To'] = email
s.send_message(msg)
s.quit()
file.write("\n\n")
file.close()









