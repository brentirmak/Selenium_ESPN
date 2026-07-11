import resend
import os
from dotenv import load_dotenv

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Retrieve the secrets using os.getenv()
resend_api_key = os.getenv("RESEND_API_KEY")
alert_recipient = os.getenv("ALERT_RECIPIENT")
alert_sender = os.getenv("ALERT_SENDER")

def init(error_name, error_snapshot, error_detail):

    # Paste your Resend API key here (or load it from Jenkins environment variables)
    resend.api_key = resend_api_key

    try:
        # 1. Read the file and encode it to binary bytes
        with open(error_snapshot, "rb") as f:
            file_content = f.read()

        params = {
            "from": f"Jenkins Alerts {alert_sender}",
            "to": [f"{alert_recipient}"],
            "subject": f"🚨 SCRIPT FAILURE ALERT - {error_name} transaction failed",
            "text": f"The script failed. Here are the details:\n\n{error_detail}",
            "attachments": [
                {
                    "filename": os.path.basename(error_snapshot),
                    "content": list(file_content)
                }
            ]
        }

        resend.Emails.send(params)
        print("Alert email sent successfully via Resend!")
    except Exception as e:
        print(f"Failed to send email alert: {e}")