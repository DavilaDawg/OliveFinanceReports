import imaplib # read the intake inbox, pull attachments
import email
import os
from email.header import decode_header

imap_server = 'imap.gmail.com'

ATTACHMENT_DIR = 'downloads'

# Map sender domains / subject keywords to a source name, so we know which
# vendor each attachment came from once we start parsing them.

SOURCE_MATCHERS = {
    'webrez': ['webrez', 'webrezpro'],
    'duetto': ['duetto'],
    'str': ['str', 'costar', 'str.com'],
    'amadeus': ['travelclick', 'ihotelier', 'amadeus'],
}

def identify_source(sender, subject):
    text = f"{sender} {subject}".lower()
    for source, keywords in SOURCE_MATCHERS.items():
        if any(kw in text for kw in keywords):
            return source
    return 'unknown'


def decode_str(value):
    if value is None:
        return ''
    decoded, encoding = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or 'utf-8', errors='ignore')
    return decoded


def read_inbox(email_address, app_password):

    if not email_address or not app_password:
        raise RuntimeError(
            "Missing REPORTS_EMAIL_ADDRESS or REPORTS_EMAIL_APP_PASSWORD "
            "environment variables. Set them before running this script."
        )

    os.makedirs(ATTACHMENT_DIR, exist_ok=True)

    mail = imaplib.IMAP4_SSL(imap_server)
    saved_files = []

    try: 
        mail.login(email_address, app_password)
        mail.select('INBOX')

        # Search for new emails in the inbox
        status, messages = mail.search(None, 'UNSEEN')

        if status != 'OK':
            print("No messages found.")
            return saved_files

        message_ids = messages[0].split()
        print(f"Found {len(message_ids)} unread messages.\n")

         # Fetch and process the latest 4 emails
        for msg_id in message_ids[-4:]:
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            if status != 'OK':
                print(f"Failed to fetch message {msg_id}")
                continue
 
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
 
            subject = decode_str(msg.get('Subject'))
            sender = decode_str(msg.get('From'))
            source = identify_source(sender, subject)
 
            print(f"Message from: {sender} | Subject: {subject} | Identified source: {source}")
 
            if not msg.is_multipart():
                continue

            # An email with an attachment has multiple parts: the body text, 
            # maybe an HTML version of the body, and then one part per attachment.
            # msg.walk() walks through every single part of that tree

            for part in msg.walk():
                content_disposition = str(part.get('Content-Disposition') or '')
                if 'attachment' not in content_disposition:
                    continue # skip non-attachment parts
 
                filename = part.get_filename()
                if not filename:
                    continue # edge case: skip parts without a filename
                filename = decode_str(filename)
 
                # Prefix with the identified source so downstream parsing
                # knows which vendor's format to expect, e.g. "webrez__report.xlsx"
                safe_filename = f"{source}__{filename}"
                filepath = os.path.join(ATTACHMENT_DIR, safe_filename) # Build the full path to save the attachment
 
                payload = part.get_payload(decode=True) # Pulls out the real file content (raw decoded bytes of the Excel)
                if payload is None:
                    continue # Skip empty excel files

                #  Take the data bytes from the excel and write them to a file in the downloads folder to be parsed later
                with open(filepath, 'wb') as f:
                    f.write(payload) 
 
                print(f"  Saved attachment: {filepath}")
                saved_files.append(filepath)
 
        return saved_files

       
            
            

    except Exception as e:
        print(f"Error connecting to the IMAP server: {e}")

    finally: 
        # Close the connection to the IMAP server
        try: 
            mail.close()
        except:
            pass
        mail.logout()

if __name__ == "__main__":
    read_inbox()
    


