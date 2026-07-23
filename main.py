from readInbox import * 
from parseData import *
from createFinalReport import *
from sendEmail import *
from dotenv import load_dotenv

load_dotenv() # workflow is erroring with this line, but it works fine when running the script locally. I think it's because the workflow is already loading the environment variables from the secrets.

email_address = os.getenv('REPORTS_EMAIL_ADDRESS')
app_password = os.getenv('REPORTS_EMAIL_APP_PASSWORD')

# Grab the exported reports from the email financereportsolive@gmail.com 

saved_files = read_inbox(email_address, app_password)

# Parse reports and extract relevant data

parsed_data = parse_reports(saved_files)

# Create new reports based on the extracted data


# Send the new reports to the appropriate recipients


