from django.shortcuts import render
from django.http import HttpResponse
import openai, os
from dotenv import load_dotenv
import speech_recognition as sr
import json
from gtts import gTTS  
from django.views.decorators.csrf import csrf_exempt

from playsound import playsound  

load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)
print(api_key)

def index(request):
    return render(request, 'blog/index.html')

def getResponse(request):
    chatResponse = None
    if api_key is not None:
        openai.api_key=api_key
        userMessage = request.GET.get('userMessage')
        prompt = userMessage
        print(userMessage)
        chatResponse = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens = 100,
            temperature =0.3
        )
    # SpeakText(chatResponse["choices"][0]["text"])
    return HttpResponse(chatResponse["choices"][0]["text"])

@csrf_exempt
def SpeakText(request):
    obj = gTTS(text=request.POST.get('Message'), lang="hi", slow=False)  
    obj.save("audio.mp3")  
    playsound("audio.mp3")  
    return HttpResponse("played")


	

def speechtotext(request):
		
	r = sr.Recognizer()
	Query = {
		"success": "False",
		"text": None
	}
	with sr.Microphone() as source:
		print('Listening')
		r.pause_threshold = 0.7
		audio = r.listen(source,phrase_time_limit=6)

	try:
		print("Recognizing")
		Query["text"] = r.recognize_google(audio)
		Query["success"] = "True"
	except Exception:
		# Query = False
		Query["text"] = "Sorry I didnt understand, can you please repeat that again."
		SpeakText(Query["text"])
	return HttpResponse(json.dumps(Query))


