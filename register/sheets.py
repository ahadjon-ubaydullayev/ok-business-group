from __future__ import print_function
import jpype
import webbrowser
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asposecells

# jpype.startJVM()
from asposecells.api import Workbook, License


def export_to_google(fileName):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials1.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # Load Excel workbook
        wb = Workbook(fileName)

        # Get worksheets collection
        collection = wb.getWorksheets()
        collectionCount = collection.getCount()

        # Get workbook and first sheet's name
        spreadsheetName = wb.getFileName()
        firstSheetName = collection.get(0).getName()

        # Create spreadsheet on Google Sheets
        spreadsheetID = create_spreadsheet(service, spreadsheetName, firstSheetName)

        # To set worksheet range
        sheetRange = None

        # Loop through all the worksheets
        for worksheetIndex in range(collectionCount):

            # Get worksheet using its index
            worksheet = collection.get(worksheetIndex)

            # Set worksheet range
            if(worksheetIndex==0):
                sheetRange= "{0}!A:Y".format(firstSheetName)
            else:
                add_sheet(service, spreadsheetID, worksheet.getName())
                sheetRange= "{0}!A:Y".format(worksheet.getName())

            # Get number of rows and columns
            rows = worksheet.getCells().getMaxDataRow()
            cols = worksheet.getCells().getMaxDataColumn()

            # List to store worksheet's data
            worksheetDatalist = []

            # Loop through rows
            for i in range(rows):
                # List to store each row in worksheet 
                rowDataList = []

                # Loop through each column in selected row
                for j in range(cols):
                    cellValue = worksheet.getCells().get(i, j).getValue()
                    if( cellValue is not None):
                        rowDataList.append(str(cellValue))
                    else:
                        rowDataList.append("")

                # Add to worksheet data
                worksheetDatalist.append(rowDataList)

            # Set values
            body = {
                'values': worksheetDatalist
            }
            
            # Execute request
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheetID, range=sheetRange,
                valueInputOption='USER_ENTERED', body=body).execute()

            # Print number of updated cells    
            print('{0} cells updated.'.format(result.get('updatedCells')))
    except HttpError as err:
        print(err)

    print("Workbook has been exported to Google Sheets.")

def create_spreadsheet(_service, _title, _sheetName):   
    # Spreadsheet details
    spreadsheetBody = {
        'properties': {
            'title': "{0}".format(_title)
        },
        'sheets': {
            'properties': {
                'title' : "{0}".format(_sheetName)
            }
        }
    }

    # Create spreadsheet
    spreadsheet = _service.spreadsheets().create(body=spreadsheetBody,
                                                fields='spreadsheetId').execute()
    
    # Open in web browser
    webbrowser.open_new_tab("https://docs.google.com/spreadsheets/d/{0}".format(spreadsheet.get('spreadsheetId')))

    return spreadsheet.get('spreadsheetId')

def add_sheet(_service, _spreadsheetID, _sheetName):
    data = {'requests': [
        {
            'addSheet':{
                'properties':{'title': '{0}'.format(_sheetName)}
            }
        }
    ]}

    # Execute request
    res = _service.spreadsheets().batchUpdate(spreadsheetId=_spreadsheetID, body=data).execute()

#  # Create a Aspose.Cells icense object
# license = License()

# # Set the license of Aspose.Cells to avoid the evaluation limitations
# license.setLicense("D:\\Licenses\\Conholdate.Total.Product.Family.lic")

export_to_google("Book1.xlsx")