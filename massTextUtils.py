from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from openpyxl.styles import PatternFill, Alignment
from flask import Flask, request
from twilio import twiml
from timeit import default_timer as timer
import time
import Pages
# Sends the same text to mass amount
# Set num_recipients < 0 to send to all numbers in file
# Client must already be declared with tokens

# Cell colors
RED = 'ff0000'
GREEN = '00ff00'
YELLOW = 'ffff00'


# Prepends country code if not present
def formatNumber(num):
    if num[0] != '+':
        num = '+1' + num  # U.S. numbers only
    return num

# Returns list of properly formatted phone numbers from excel sheet


def populateNumberList(sheet):
    max_row = sheet.max_row
    numList = []
    for i in range(1, max_row + 1):
        cellObj = sheet.cell(row=i, column=1)
        number = str(cellObj.value)
        numList.append(formatNumber(number))
    return numList


# Tracks used numbers in excel sheet, marks yellow if sent
def markSentExcel(num, sheet, color):
    # TODO - find number in sheet, mark as used
    count = 1
    for row in range(1, sheet.max_row + 1):
        cellObj = sheet.cell(row=row, column=1)  # Phone number
        cellColor = sheet.cell(row=row, column=2)  # Status color
        if str(cellObj.value) == num.replace("+1", ""):
            cellColor.fill = PatternFill(
                start_color=color, end_color=color, fill_type="solid")
            if color == GREEN:
                cellColor.value = "SENT"
            else:
                cellColor.value = "FAIL"
            cellColor.alignment = Alignment(horizontal='center')
            break
        count += 1

# Send same message to entire list
# msg - message to mass send; client - twilio client; numbers - list of numbers as strings
# twil_num - twilio number to send msg from; sheet - excel sheet for marking sent


def massSendSMS(msg, numbers, sheet, self):
    start = timer()
    count = 1
    output = None
    for num in numbers:
        try:
            self.client.messages.create(body=msg, from_=self.twil_num, to=num)
        except:
            markSentExcel(num, sheet, RED)
            output = "Message send failure to " + num
        else:
            markSentExcel(num, sheet, GREEN)
            output = "Message sent to " + num
        if self.surpress_ckbx.isChecked() == False:
            self.output_textbox.appendPlainText(output)
        self.progress.setValue((count/len(numbers)) * 100)
        QApplication.processEvents()
        count += 1
        time.sleep(0.3)
    end = timer()
    return end - start
