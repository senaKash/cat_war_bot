from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import datetime
from datetime import timedelta

##SAMPLE_RANGE_NAME = 'Лист1!A2:E246'

class GoogleSheet:
    SPREADSHEET_ID = '126noVJN4ZyCBl4zn98kVhaL8BtSPxg2JzXjoM0CHlZQ'
    #SPREADSHEET_ID = '1ZAI3yqSutwUB5hV4phLSZtCvDds7E3-k_FprhJZEOYo'
    #SHEEEET = '1K7V5kWP1szwl0haS1Den7avejhT96OjXGCDR-4tZ4zY'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def coopAdd(self, id, name, tableName):
        idMass = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = f'{tableName}!B2:B'
        ).execute()
        #print(len(idMass['values']))
        res = []
        for x in idMass['values']:
                res.extend(x if isinstance(x, list) else [x])
        #print(len(res))
        try:
            ind = res.index(str(id))
            range = f'{tableName}!A{ind+2}'

            
            data = [{
            'range': range,
            'values': [[name]]
            }]

            body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
            }
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
            return 1
        except:

            range = f"{tableName}!A{len(res)+2}:B{len(res)+2}"

            data = [{
            'range': range,
            'values': [[name, str(id)]]
            }]

            body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
            }
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
            return 0

    def addToBd(self, id, name):
        isTrue = self.coopAdd(id, name, "Главная.")
        self.coopAdd(id, name, "За период")
        return isTrue
        '''
        idMass = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = 'Главная.!B2:B'
        ).execute()
        #print(len(idMass['values']))
        res = []
        for x in idMass['values']:
                res.extend(x if isinstance(x, list) else [x])
        #print(len(res))
        try:
            ind = res.index(str(id))
            range = f"Главная.!A{ind+2}"

            
            data = [{
            'range': range,
            'values': [[name]]
            }]

            body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
            }
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
            return 1
        except:

            range = f"Главная.!A{len(res)+2}:B{len(res)+2}"

            data = [{
            'range': range,
            'values': [[name, str(id)]]
            }]

            body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
            }
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        
        '''
        '''

        range = f'Главная.!A{ind+2}'

        name = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = range
        ).execute()
        print(name)

        res = []
        for x in name['values']:
            res.extend(x if isinstance(x, list) else [x])
        print(res)
        strName = ''.join(res)
        return strName
        '''

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def findInd(self, id):
        idMass = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = 'Главная.!B2:B'
        ).execute()
        res = []
        
        for x in idMass['values']:
            res.extend(x if isinstance(x, list) else [x])
        ind = res.index(str(id))

        range = f'Главная.!A{ind+2}'

        name = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = range
        ).execute()
        #print(name)

        res = []
        for x in name['values']:
            res.extend(x if isinstance(x, list) else [x])
        #print(res)
        strName = ''.join(res)
        return strName

    def insertInMain(self, rnB, id, values):

        ind = self.findInd(id)

        #range = f'Главная!{rnB}{ind + 1}:{rnB}{ind+3}'
        range = f'Главная!{rnB}{ind + 2}'
        #print(range)
        
        count = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = range
        ).execute()
        #print(count)
        #print(int(count['values']))
        
        res = []
        for x in count['values']:
            res.extend(x if isinstance(x, list) else [x])
        
        print(int(res[0]) + values)
        
        
        body = {
            'value_input_option': 'USER_ENTERED', # RAW
            'data': [
                {'range': range, 'values': [[f'{int(res[0])+values}']]}
            ]
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        

    def insertRow(self, range, values):
        

        self.addRow()

        body = {
            'value_input_option': 'USER_ENTERED', # RAW
            'data': [
                {'range': range, 'values': values}
            ]
        }
        #result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
    def addRow(self):
        request_body = {
            'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': 127369550,
                        'dimension': 'ROWS',
                        'startIndex': 1,
                        'endIndex': 2
                    }
                }
            }
            ]
        }
        result = self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=request_body).execute()
    def delFromStat(self, id):
        idMass = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = 'Статистика!F2:F'
        ).execute()
        #idMass['values']
        
        res = []
        #try:
        for x in idMass['values']:
            res.extend(x if isinstance(x, list) else [x])
        #print(res)
        #print(res.index('647'))
        ind = res.index(str(id))
            
        body = {
                'requests':[
                {
                    'deleteDimension':{
                        'range':{
                            'sheetId': 127369550,
                            'dimension': 'ROWS',
                            'startIndex': ind+1,
                            'endIndex': ind+3
                        }
                    }
                }
                ]
            }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        #except:
        #    pass
        #print(res)
        #print(res.index('647'))
        #print(idMass['values'].index('647'))
    def stat(self, id, full):
        dataStat = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range = 'За период!B1:F1'
        ).execute()
        #print(dataStat)
        #print(dataStat['values'][0][0])
        #print(dataStat['values'][0][2])
        #dates = []
        dataLeft = datetime.datetime.strptime(dataStat['values'][0][0], "%d.%m.%Y").date()
        dataRight = datetime.datetime.strptime(dataStat['values'][0][4], "%d.%m.%Y").date()
        #dates.append(datetime.datetime.strptime(dataStat['values'][0][0], "%d.%m.%Y").date())
        #dates.append(datetime.datetime.strptime(dataStat['values'][0][2], "%d.%m.%Y").date())
        #dates[0] = dates[0] + timedelta(days=1)
        #print(dates)

        dataOld = datetime.datetime.strptime("01.01.2003", "%d.%m.%Y").date()
        
        


        current_date = datetime.datetime.now()
        combDate = datetime.datetime.combine(dataRight, datetime.time(0, 0))



        if combDate < current_date:
            
            dataLeft += timedelta(days=7)
            dataRight += timedelta(days=7)
            body = {
                        'value_input_option': 'USER_ENTERED', # RAW
                        'data': [
                        {'range': 'За период!B1:F1', 'values': [[f'{dataLeft.strftime("%d.%m.%Y")}', '', '', 'по', f'{dataRight.strftime("%d.%m.%Y")}']]}
                        ]
                    }
            result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
            
        else:
            if(full == True):
                body = {
                    'value_input_option': 'USER_ENTERED', # RAW
                    'data': [
                    {'range': 'За период!B1', 'values': [[f'{dataOld.strftime("%d.%m.%Y")}']]}
                    ]
                }
                result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()

                
            idMass = self.service.spreadsheets().values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range = 'За период!B4:B'
            ).execute()
            res = []
            
            for x in idMass['values']:
                res.extend(x if isinstance(x, list) else [x])
            ind = res.index(str(id))

            #print(ind)

            range = f'За период!C{ind+4}:T{ind+4}'

            name = self.service.spreadsheets().values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range = range
                ).execute()

            if(full == True):
                body = {
                    'value_input_option': 'USER_ENTERED', # RAW
                    'data': [
                    {'range': 'За период!B1', 'values': [[f'{dataLeft.strftime("%d.%m.%Y")}']]}
                    ]
                }
                result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()   

            #print(name)    
            
            return name['values'], dataLeft.strftime("%d.%m.%Y"), dataRight.strftime("%d.%m.%Y") 
        #print(combDate)
        '''
        dataRight += timedelta(days=1)
        #print(dataRight.strftime("%d.%m.%Y"))

        body = {
            'value_input_option': 'USER_ENTERED', # RAW
            'data': [
                {'range': 'За период!B1:D1', 'values': [[f'{dataLeft.strftime("%d.%m.%Y")}', 'по', f'{dataRight.strftime("%d.%m.%Y")}']]}
            ]
        }
        
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        '''