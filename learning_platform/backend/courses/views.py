from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
import io

# Create your views here.

def course_detail(request, course_id):
    return render(request, 'course_detail.html', {'course_id': course_id})

def speak_view(request):
    text = request.GET.get('text','')
    
    if not text:
        return HttpResponse("Brak tekstu do przeczytania", status = 400)
    
    tts = gTTS(text=text, lang='pl')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return HttpResponse(mp3_fp.read(), content_type="audio/mpeg")
