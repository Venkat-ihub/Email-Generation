from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.conf import settings

# Configure the Google Generative AI client
genai.configure(api_key=settings.GENAI_API_KEY)

ALLOWED_MAIL_TYPES = ["Regular Mail", "Cold Mail", "Follow-Up Mail", "Waitlist Mail"]
ALLOWED_TONES = ["Professional/Corporate", "Friendly/Conversational", "Urgent/Direct", "Persuasive/Sales"]

def email_response_generator(request):
    if request.method == "POST":
        incoming_email = request.POST.get("incoming_email", "").strip()
        mail_type = request.POST.get("mail_type", "Regular Mail")
        mail_tone = request.POST.get("mail_tone", "Professional/Corporate")

        if not incoming_email:
            return JsonResponse({"error": "Incoming email is required."}, status=400)
        if mail_type not in ALLOWED_MAIL_TYPES or mail_tone not in ALLOWED_TONES:
            return JsonResponse({"error": "Invalid mail type or tone."}, status=400)

        try:
            prompt = f"Generate a {mail_type.lower()} in a {mail_tone.lower()} tone for the following email:\n\n{incoming_email}"
            response = genai.generate_text(prompt=prompt)

            if response and response.candidates:
                generated_subject = f"Re: {mail_type}"
                generated_email = response.candidates[0]['content']

                return JsonResponse({
                    "subject": generated_subject,
                    "body": generated_email,
                })
            else:
                return JsonResponse({"error": "No response generated from the API."}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Error generating email: {str(e)}"}, status=500)

    return render(request, "email_app/email_form.html")
