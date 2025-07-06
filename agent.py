OPENAI_API_KEY = "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"

#   ""step - 1"""


# # Initialize OpenAI client
# openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Load your service info
# with open("services.txt", "r") as f:
#     SERVICE_INFO = f.read()

# def classify_intent(email_content: str) -> str:
#     """Ask OpenAI: should we 'meeting', 'info', or 'ignore'?"""
#     resp = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are an email triage assistant."},
#             {"role": "user", "content": (
#                 "Classify this email into one of exactly three categories:\n"
#                 "  • meeting  (they want to talk or schedule a meeting)\n"
#                 "  • info     (they want pricing or service details)\n"
#                 "  • ignore   (they decline or no next steps)\n\n"
#                 f"Email:\n\"\"\"\n{email_content}\n\"\"\"\n"
#                 "Reply with exactly one word: meeting, info, or ignore."
#             )}
#         ]
#     )
#     return resp.choices[0].message.content.strip().lower()

# def generate_meeting_reply(email_content: str) -> str:
#     """Generate a polite meeting‑proposal reply."""
#     resp = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are an assistant that writes professional email replies."},
#             {"role": "user", "content": (
#                 "The sender wrote:\n"
#                 f"\"\"\"\n{email_content}\n\"\"\"\n\n"
#                 "Draft a concise reply proposing 2–3 time slots (in their timezone) next week,"
#                 " expressing enthusiasm, and asking which works best."
#             )}
#         ]
#     )
#     return resp.choices[0].message.content.strip()

# def generate_info_reply() -> str:
#     """Return the static service info."""
#     return f"Hello,\n\nThank you for your interest. Here’s our service overview:\n\n{SERVICE_INFO}\n\nBest regards."

# def handle_email(email_content: str) -> str | None:
#     """
#     Main function.
#      - Returns the reply text if intent is 'meeting' or 'info'.
#      - Returns None if 'ignore'.
#     """
#     intent = classify_intent(email_content)

#     if intent == "meeting":
#         return generate_meeting_reply(email_content)
#     elif intent == "info":
#         return generate_info_reply()
#     else:
#         # ignore → no response
#         return None



# ""step - 2""



# # agent.py
# import os
# import dateparser
# from datetime import timedelta
# from openai import OpenAI

# # OpenAI setup
# openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Load service info
# with open("services.txt", "r") as f:
#     SERVICE_INFO = f.read()

# def classify_intent(email_content: str) -> str:
#     """Return: meeting, info, or ignore"""
#     response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You classify emails into: meeting, info, or ignore."},
#             {"role": "user", "content": f"Classify this:\n\"\"\"\n{email_content}\n\"\"\""}
#         ]
#     )
#     return response.choices[0].message.content.strip().lower()

# # def extract_datetime(email_content: str):
# #     """Use dateparser to extract datetime from free text"""
# #     dt = dateparser.parse(email_content, settings={'PREFER_DATES_FROM': 'future'})
# #     return dt

# from openai import OpenAI
# import dateparser
# from datetime import datetime

# openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def extract_datetime(email_content: str) -> datetime | None:
#     """Try dateparser first. If that fails, use GPT to extract ISO datetime."""
#     dt = dateparser.parse(
#         email_content,
#         settings={
#             'TIMEZONE': 'Asia/Kolkata',
#             'TO_TIMEZONE': 'Asia/Kolkata',
#             'RETURN_AS_TIMEZONE_AWARE': True,
#             'PREFER_DATES_FROM': 'future',
#             # Removed RELATIVE_BASE — this causes TypeError
#         }
#     )

#     if dt:
#         return dt

#     print("⚠️ dateparser failed. Trying GPT-based datetime extraction...")

#     # Ask GPT to extract ISO format date
#     response = openai.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {
#             "role": "system",
#             "content": (
#                 "You are an expert assistant. From the email content, extract the exact date and time "
#                 "for the meeting in ISO 8601 format (e.g., 2025-07-10T15:30:00+05:30). "
#                 "Assume IST timezone. If the email only says 'Thursday', assume the next Thursday from today. "
#                 "If no valid date/time is mentioned, return: none"
#             ),
#         },
#         {
#             "role": "user",
#             "content": f"Email content:\n\"\"\"\n{email_content}\n\"\"\"\n\nReturn only the datetime in ISO format:",
#         },
#     ],
# )


#     extracted = response.choices[0].message.content.strip()
#     print("🧠 GPT extracted:", extracted)


#     if extracted.lower() == "none":
#         return None

#     try:
#         # Try parsing GPT-extracted datetime
#         return dateparser.parse(
#             extracted,
#             settings={
#                 'TIMEZONE': 'Asia/Kolkata',
#                 'TO_TIMEZONE': 'Asia/Kolkata',
#                 'RETURN_AS_TIMEZONE_AWARE': True,
#             }
#         )
#     except Exception as e:
#         print("❌ Failed to parse GPT-provided datetime:", e)
#         return None



# def create_calendar_event(calendar, email_content: str, sender: str = "Client") -> str:
#     dt = extract_datetime(email_content)
#     if not dt:
#         return "❌ Couldn't find a date/time in the email. Please reply to reschedule."

#     end = dt + timedelta(minutes=30)

#     event = {
#         'summary': f'Meeting with {sender}',
#         'description': email_content,
#         'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
#         'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
#     }

#     created_event = calendar.events().insert(calendarId='primary', body=event).execute()
#     return f"✅ Meeting scheduled on {dt.strftime('%A, %d %B %Y at %I:%M %p')} IST."

# def generate_info_reply() -> str:
#     return f"Hi,\n\nThanks for reaching out. Here’s our service info:\n\n{SERVICE_INFO}\n\nLet me know if you’d like to connect further."

# def handle_email(email_content: str, calendar=None, sender="Client") -> str | None:
#     intent = classify_intent(email_content)

#     if intent == "meeting":
#         if calendar:
#             return create_calendar_event(calendar, email_content, sender)
#         else:
#             return "🕑 I would schedule a meeting here, but calendar integration is off."

#     elif intent == "info":
#         return generate_info_reply()

#     else:
#         return None









import os
import dateparser
from datetime import datetime, timedelta
from openai import OpenAI
from googleapiclient.discovery import Resource

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("services.txt", "r") as f:
    SERVICE_INFO = f.read()




import re
import pytz
import dateparser
from datetime import datetime, timedelta
from googleapiclient.discovery import build, Resource


WEEKDAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

def get_next_weekday(target_weekday: int, hour: int, minute: int):
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    days_ahead = (target_weekday - now.weekday() + 7) % 7 or 7
    next_day = now + timedelta(days=days_ahead)
    return next_day.replace(hour=hour, minute=minute, second=0, microsecond=0)

def extract_datetime(email_content: str) -> datetime | None:
    # Try direct parse first
    dt = dateparser.parse(
        email_content,
        settings={
            'TIMEZONE': 'Asia/Kolkata',
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now(pytz.timezone("Asia/Kolkata")),
            'RETURN_AS_TIMEZONE_AWARE': True
        }
    )
    if dt:
        print(f"🧠 dateparser matched: {dt}")
        return dt

    # Try regex for weekday + time (e.g., "this Friday at 3 PM")
    weekday_match = re.search(
        r"\b(this\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow)\b",
        email_content,
        re.I
    )
    time_match = re.search(r"(\d{1,2}(:\d{2})?\s*(am|pm|AM|PM))", email_content)

    if weekday_match and time_match:
        weekday_raw = weekday_match.group(0).lower().strip()
        time_raw = time_match.group(1)
        print(f"🧠 Regex matched: {weekday_raw}, {time_raw}")

        parsed_time = dateparser.parse(time_raw)
        if not parsed_time:
            print("⚠️ Failed to parse time string")
            return None

        if "tomorrow" in weekday_raw:
            weekday = (datetime.now(pytz.timezone("Asia/Kolkata")) + timedelta(days=1)).weekday()
        else:
            weekday = WEEKDAY_MAP[weekday_match.group(2).lower()]

        return get_next_weekday(weekday, parsed_time.hour, parsed_time.minute)

    print("⚠️ dateparser and regex failed. Trying GPT fallback...")

    # GPT fallback
    try:
        from openai import OpenAI
        openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract the datetime from the email and return in ISO 8601 format with time zone as +05:30 (IST). If none, say 'none'."},
                {"role": "user", "content": email_content}
            ]
        )
        iso = response.choices[0].message.content.strip()
        print(f"🧠 GPT extracted: {iso}")
        if iso.lower() == "none":
            return None
        return datetime.fromisoformat(iso)
    except Exception as e:
        print(f"❌ GPT fallback failed: {e}")
        return None





# ---------- Create Calendar Event ----------
def create_calendar_event(calendar: Resource, email_content: str, sender: str = "Client") -> str:
    dt = extract_datetime(email_content)
    if not dt:
        return "❌ Couldn't find a date/time in the email. Please reply to reschedule."

    # Validate if the date is in the past
    if dt < datetime.now(dt.tzinfo):
        return "❌ The extracted date/time is in the past. Please suggest a future time."

    end = dt + timedelta(minutes=20)

    event = {
        'summary': f'Meeting with {sender}',
        'description': email_content,
        'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    calendar.events().insert(calendarId='primary', body=event).execute()

    # Return a realistic reply to send via email
    return (
        f"Subject: Meeting Confirmed\n\n"
        f"Hi {sender},\n\n"
        f"Thanks for your email. I’ve scheduled our 20-minute call for "
        f"**{dt.strftime('%A, %d %B %Y at %I:%M %p IST')}**.\n"
        f"Looking forward to connecting!\n\n"
        f"Best regards,\n"
        f"[Your Name]\n[Your Position]\n[Your Company]"
    )


# ---------- Info Request Reply ----------
def generate_info_reply() -> str:
    return f"Hi,\n\nThanks for reaching out. Here’s our service info:\n\n{SERVICE_INFO}\n\nLet me know if you’d like to connect further."


# ---------- Entry handler ----------
def handle_email(email_content: str, calendar=None, sender="Client") -> str | None:
    intent = classify_intent(email_content)

    if intent == "meeting":
        if calendar:
            return create_calendar_event(calendar, email_content, sender)
        else:
            return "🕑 I would schedule a meeting here, but calendar integration is off."

    elif intent == "info":
        return generate_info_reply()

    else:
        return None



# # ---------- Intent classifier ----------
def classify_intent(email_content: str) -> str:
    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an email intent classifier. "
                "Classify the following email as one of these intents:\n\n"
                "- 'meeting': if the sender is trying to schedule a call or meeting\n"
                "- 'info': if the sender is asking about services, pricing, features, capabilities, etc.\n"
                "- 'ignore': if the email is not relevant, spam, or a negative response\n\n"
                "Respond with only one word: meeting, info, or ignore."
            )
        },
        {"role": "user", "content": f"{email_content}"}
    ]
)

    return response.choices[0].message.content.strip().lower()




