from curl_cffi import requests

import imaplib, email


class EmailManager(requests.Session):
    """
    Buy Emails from antibotmail.com
    """

    def __init__(self, apiKey: str):
        super().__init__()
        self.apiKey = apiKey
        self.getEmail()

    def getEmail(self):
        response = self.post(
            "https://api.antibotmail.com/api/mail/buy",
            json={
                "mailcode": "OUTLOOK_TEMP",
                "quantity": 1,  # daniellehawkins22240@outlook.com
                "X-ABM-ApiKey": self.apiKey,
            },
        ).json()
        if response.get("success"):
            self.email = response.get("Data").get("Emails")[0].get("Email")
            self.password = response.get("Data").get("Emails")[0].get("Password")
            return self.email, self.password
        else:
            return self.getEmail()

    def get(self, e, password):
        while True:
            try:

                IMAP_SERVER = "imap.outlook.com"
                mail = imaplib.IMAP4_SSL(IMAP_SERVER)
                mail.login(e, password)
                mail.select("INBOX")

                # Search for a specific email based on criteria (e.g., subject)
                result, data = mail.search(
                    None, '(SUBJECT "Verify Email Address for Discord")'
                )

                # Get the unique identifier (UID) of the first email found
                email_ids = data[0].split()
                if email_ids:
                    latest_email_id = email_ids[-1]

                    # Fetch the email with the given UID
                    result, email_data = mail.fetch(latest_email_id, "(RFC822)")
                    raw_email = email_data[0][1]

                    # Parse the email using the email library
                    msg = email.message_from_bytes(raw_email)

                    # Extract plain text content from the email
                    plain_text_content = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                plain_text_content += part.get_payload(
                                    decode=True
                                ).decode(part.get_content_charset(), "ignore")
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            plain_text_content += msg.get_payload(decode=True).decode(
                                msg.get_content_charset(), "ignore"
                            )
                    mail.logout()
                    return plain_text_content.split("Verify Email: ")[1].strip()
                else:
                    continue
            except Exception as e:
                print(e)
                return "TIMEOUT"

    def getDiscordEmail(self):
        verify_code = self.get(self.email, self.password)
        res = (
            requests.get(
                verify_code,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US",
                    "Connection": "keep-alive",
                    "DNT": "1",
                    "Host": "click.discord.com",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
                },
            )
            .headers.get("Location")
            .split("=")[1]
        )
        print(res)
        return res
