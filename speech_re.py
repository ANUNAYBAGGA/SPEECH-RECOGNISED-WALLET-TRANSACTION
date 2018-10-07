import speech_recognition as sr

def recog():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say anything : ")
        print("Listening.....")
        audio = r.listen(source,phrase_time_limit = 3)
        print("Recognizing......")
        try:
            text = r.recognize_google(audio)
            print("You said : {}" , format(text))
            text = text.lower()
            l = text.split(" ")
            print(l)
            return (l[1],int(l[2]))

        except:
            print("Could not recognize that")
            temp = "try again could not recognize your voice, try to say in this format ' send 'username' 'amount' rupees' "
            return(temp,0)
