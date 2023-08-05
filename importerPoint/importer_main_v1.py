##############################
#GrandShake Importer Script
#Author - Ayush Raj
#Version 1.5
##############################


#Import the required libs for this script.
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import requests
import json
import base64

## This part handles the access to the Google Sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/root/node/genesisfiles/files/importerPoint/test-project-1-349705-bf9bfec03f61.json", scope)
client = gspread.authorize(creds)


## Here we point to the worksheets that we need
firstSheet = client.open("Algo Grandshake database").worksheet('Sheet1')
secondSheet = client.open("Algo Grandshake database").worksheet('Sheet2')

## This part will retrieve information from the AlgoNetwork
base_url = 'https://algoindexer.testnet.algoexplorerapi.io/v2/transactions/{i}'
tx_file = open("/root/node/genesisfiles/files/transactionsFile.txt", "r")
output = tx_file.readlines()
tx_list = []
tx_dict_list = []

## This part loops over every tx IDs in a tx_file and extracts all the transaction details for each ID and filters the relevant ones
for i in output:
    tx_list.append(i.replace('\n', ''))

for i in tx_list:
    url = base_url.format(i=i)
    response = requests.get(url).text
    json_response = json.loads(response)
    
    # Transaction amount
    tx_amount = json_response['transaction']['asset-transfer-transaction']['amount']
    
    # Asset ID
    asset_id = json_response['transaction']['asset-transfer-transaction']['asset-id']
    
    # Reciever ID
    rx_id = json_response['transaction']['asset-transfer-transaction']['receiver']
    
    # Sender ID
    snd_id = json_response['transaction']['sender']
    
    # Note containing enrollment ID, Uniqu ID and amount to transfer
    note = json_response['transaction']['note']
    
    # Converting the base64 format of note to ascii format
    base64_string = str(note)
    base64_bytes = base64_string.encode("ascii")
    note = base64.b64decode(base64_bytes)
    Note = note.decode("ascii")
    notes = []
    
    # Extracting Enrollment ID, Amount to transfer and Unique ID 
    for item in Note.split("/"):
        for element in item.split("-"):
            notes.append(element)
            Enrollment_ID = notes[1]
    Amount_to_transfer = notes[3]
    Unique_ID = notes[5]
    
    # Creating an empty dictionary to store all the relevant transaction details
    Tx_dict = dict()
    Tx_dict["Transaction ID"] = i
    Tx_dict["Sender address"] = snd_id
    Tx_dict["Receiver address"] = rx_id
    Tx_dict["Assest ID"] = asset_id
    Tx_dict["Token amount"] = tx_amount
    Tx_dict["Enrollment ID"] = Enrollment_ID
    Tx_dict["Amount to be transferred"] = Amount_to_transfer
    Tx_dict["Unique ID"] = Unique_ID
    
    # Based on Enrollment ID for a given google sheet, displaying the corresponding transaction ID along with the token amount
    txn_id = Tx_dict["Transaction ID"]
    enrollId = Tx_dict["Enrollment ID"]
    tokenAmount = Tx_dict["Token amount"]
    cell = str(secondSheet.find(str(enrollId)))
    location = cell.split(' ')[1]
    cellCord = location.split('R')[1].split('C')[0]
    secondSheet.update_cell(cellCord, 6, txn_id)
    secondSheet.update_cell(cellCord, 5, tokenAmount)
