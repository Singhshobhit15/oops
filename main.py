# from agent import handle_email

# if __name__ == "__main__":
#     # ── Example incoming email ──
#     email_body = """
#     Hi,

# Thanks for getting back to me.

# I’d love to chat further and understand how your solution could help our internal workflows. Would you be available for a quick 20-minute call on **Thursday at 3:30 PM IST**?

# If that time doesn’t work, feel free to suggest an alternative.

# Looking forward to our conversation.

# Best,  
# Ankit Verma  
# CTO | BrightFrame Analytics  
# ankit@brightframe.io

#     """

#     reply = handle_email(email_body)

#     if reply:
#         print("=== AGENT REPLY ===\n")
#         print(reply)
#     else:
#         print("No response needed (ignore).")


# main.py
from google_auth import get_calendar_service
from agent import handle_email

if __name__ == "__main__":
    email_body = """
   Hi team,

We’re exploring automation tools to help manage our inbound lead flow. Can you share more about what your AI assistant can do and how your pricing works?

Best,  
Zane Fernandes  
Sales Enablement | MobiCore


    """

    calendar = get_calendar_service()
    reply = handle_email(email_body, calendar, sender="Ankit Verma")

    if reply:
        print("=== AGENT REPLY ===\n")
        print(reply)
    else:
        print("No response needed (ignored).")
