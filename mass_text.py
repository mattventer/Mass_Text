from twilio.rest import Client
import openpyxl
import sys
import massTextUtils as utils

###############################################################################
###############################################################################
# Input from GUI

# Your Account SID from twilio.com/console
account_sid = "AC46a0f4b48f6b2e8b6e747655d13989ca"
# Your Auth Token from twilio.com/console
auth_token = "3e0a252ed3aa63810cda0a237cef6d9b"
# Number that the texts will be sent from
send_num = "4752074435"
#Test
msg_data = "testttttt"
#Filepath to stored number list

try:
    filename = sys.argv[1]
except:
    print("Error: Must include '.xlsx' file path.")
    print("Correct format is: 'python3 mass_text.py <number_list.xlsx>'")
else:
    print("Starting...")


###############################################################################
###############################################################################
# Obj Declarations
client = Client(account_sid, auth_token)


###############################################################################
###############################################################################
# Main
# Send msg
num_list = utils.populateNumberList(num_sheet)
utils.massSendSMS(msg_data, client, num_list, send_num, num_sheet)
wb.save(filename)

   



