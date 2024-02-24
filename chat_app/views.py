from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
# Create your views here.

genai.configure(api_key="AIzaSyC7c4aJ6p3XlM_76QpuN5WnosaXZMD9tcI")

@login_required
def ask_question(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(text)
            user = request.user 
            ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
            response_data = {
                "text": response.text,
            }
            return JsonResponse({"data": response_data})
        except StopCandidateException as e:
            print(f"StopCandidateException raised: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return JsonResponse({"error": "Unsupported method. Only POST requests are allowed."}, status=405)
        return HttpResponseRedirect(
            reverse("chat")
        )
    
@login_required
def chat(request):
    user = request.user 
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chat_bot.html", {"chat": chats})