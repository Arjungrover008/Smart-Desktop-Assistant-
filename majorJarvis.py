import pyttsx3
import speech_recognition as sr
import datetime
import pytz
import webbrowser
import wikipedia
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import Message
from email import encoders
import pyautogui
import requests
import pyjokes
import time
import cv2 
import wolframalpha
from googletrans import Translator
from gtts import gTTS
import psutil

engine = pyttsx3.init('sapi5') # sapi5 is a speech API by Microsoft
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[0].id)

def speak (audio):
    engine.say(audio)
    engine.runAndWait()

#A function to greet
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !!")
    elif hour>= 12 and hour < 18:
        speak("Good Afternoon !!")
    else:
        speak("Good Evening !!")
    
    speak ("Hi there ")

# Function to read top 5 news
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=163ae0d806b94ffab0eaa27074a03032'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    n = ["1","2", "3", "4", "5"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(n)):
        speak(f" {head[i]}")

#Function to know the battery of the system
def battery():
    battery = psutil.sensors_battery().percent
    speak(f"Your system has {battery} % of battery left")

#Function to take a screenshot
def screenshot():
    img = pyautogui.screenshot()
    speak("Hold the screen for few seconds ")
    img.save("C://Users//DELL//Desktop//js.jpg")
    speak("The screenshot has been taken ")

#Function to send an email
def email():
    email = '_________________________'
    password = '**********************'
    send_to_email = '___________________'
    
    # to know the subject
    speak("Tell me the subject of this email")
    query3 = takeCommand().lower()
    subject = query3

    # to know the message of this email
    speak("And tell me the message to send")
    query2 = takeCommand().lower()
    message = query2

    # to know the path of the attachment
    speak("Enter the path of the file to be attached")
    file_location = input("Please enter the path: ")

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()





# Function to take commands from the user and convert it to string format
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        r.adjust_for_ambient_noise(source, duration = 1)
        print("HOW MAY I HELP YOU  ?? ")
        r.pause_threshold = 1
        audio = r.listen(source)

    query = "" 
    try:
        print("Recognizing....")    
        query = r.recognize_google(audio).lower() #Using google for voice recognition
        print(query)
        
        
    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query

app = wolframalpha.Client("APAR5Y-PTX7W85YR9")       

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower()

        #---------------------------------------------to open wikipedia-------------------------------------------------------
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        #---------------------------------------------to open youtube-------------------------------------------------------
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        #---------------------------------------------to open notepad-------------------------------------------------------
        
        elif 'open notepad' in query:
            path = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(path)

        #---------------------------------------------to close notepad------------------------------------------------------
        
        elif 'close notepad' in query:
            speak("Closing notepad")
            os.system("taskkill /f /im notepad.exe")
            
        #----------------------------------------------to open google-------------------------------------------------------
       
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        #-----------------------------------------to open UPES Bloackboard--------------------------------------------------
       
        elif 'open blackboard' in query:
            webbrowser.open("blackboard learn upes.com")
            
        #---------------------------------------------to play music---------------------------------------------------------
       
        elif 'play music' in query:
            music_dir = "C:\\Users\\DELL\\Music\\Songs"
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
            
        #---------------------------------------------to open gmail---------------------------------------------------------
       
        elif 'open gmail' in query:
            webbrowser.open("gmail.com")
            

        #-------------------------------------------to tell the time--------------------------------------------------------
        
        elif 'time' in query:
            strt = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strt}")
            speak(f"The time is {strt}")

        #------------------------------------------to tell today's date-----------------------------------------------------

        elif 'date' in query:
            d = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata'))
            dt = d.strftime('%d %B, %Y')
            print("Today's date is: " +dt)
            speak(f"Today's date is {dt}")
            
        #--------------------------------------------to tell a joke---------------------------------------------------------
        
        elif 'joke' in query: 
            speak(pyjokes.get_joke())
        
        #----------------------------------------to tell todays headlines----------------------------------------------------
        
        elif 'headlines' in query:
            speak("Fetching the latest news")
            speak("Todays headlines are ")
            news()

        #---------------------------------------to switch between windows---------------------------------------------------
        
        elif 'switch the window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(5)
            pyautogui.keyUp("alt")

        #----------------------------------------to shut down the system---------------------------------------------------
        
        elif 'shut down' in query:
            os.system("shutdown /s /t 5")

        #----------------------------------------------to open camera------------------------------------------------------
        
        elif 'open camera' in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('camera', img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        #---------------------------------------to tell the current location----------------------------------------------
        
        elif 'location' in query:
            speak("Let me check your current location")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"According to me, your current location is {city} in {country}")
            except Exception as e:
                speak("Sorry, I am not able to find your current location")
                pass
        
        #------------------------------------------to tell the temperature-------------------------------------------------
        
        elif 'temperature' in query:
            temp = app.query(query)
            speak("Temperature here is: ")
            speak(next(temp.results).text)

        #-------------------------------------to perform mathematical calculations-----------------------------------------

        elif 'calculate' in query:
            speak("What should I calculate ?")
            query = takeCommand().lower()
            calc = app.query(query)
            speak("The answer is: ")
            speak(next(calc.results).text)            

        #--------------------------------------------to search on browser--------------------------------------------------

        elif 'search on chrome' in query:
            speak("What should I search ? ")
            search = takeCommand().lower()
            chrompath = 'C://Program Files (x86)//Google//Chrome//Application//chrome.exe %s'
            webbrowser.get(chrompath).open(search+'.com')

        #------------------------------------------battery of the system---------------------------------------------------
        
        elif 'battery' in query:
            battery()

        #-------------------------------------------to take a screenshot----------------------------------------------------
        
        elif 'screenshot' in query:
            screenshot()

        #---------------------------------------------to send email---------------------------------------------------------  
        elif 'send email' in query:

                email()
                speak("Email has been sent successfully")
            
                

        elif 'translate' in query:
            query = takeCommand().lower()
            translator = Translator()
            from_lang = 'en'
            to_lang = 'hi'
            speak("What should I translate ?")

            try:
                text_to_translate = translator.translate(query, src = from_lang, dest = to_lang)
                text = text_to_translate.text
                speak = gTTS(text = text, lang = to_lang, slow=False)
                speak.save("captured_voice.mp3")
                os.system("start captures_voice.mp3")
            except sr.UnknownValueError:
                speak("Unable to understand the voice")
            except sr.RequestError as e:
                print(e)        

        
        #-------------------------------------------to quit the system---------------------------------------------------------------------------------
       
        elif 'quit' in query:
            speak("OKAY Bye")
            break
        
