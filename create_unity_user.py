# coding: utf-8
from getpass import getpass
import requests
requests.packages.urllib3.disable_warnings()
import json



EMC_Unity_IP = raw_input('your EMC Unity IP Address: ')
#EMC_Unity_IP = "10.44.131.184"
URL = 'https://' + EMC_Unity_IP  + '/api/types/user/instances'
USER = raw_input('Enter Unity\'s admin name: ')
#USER = "admin"
PASSWORD = getpass('Enter Unity\'s admin password: ')
#PASSWORD = "Passw0rd!"


s = requests.Session()
HEADERS = {'X-EMC-REST-CLIENT': 'true'}

def printUsers():
  r = s.get(URL, headers = HEADERS, auth=(USER, PASSWORD), verify=False)
  users = []
  if r.status_code == 200:
      print('Successed to login to EMC Unity')
      print(r.status_code)
      print
      a = json.loads(r.text)
      entries = a['entries']
      print("This EMC Unity are registered following users now")
      for entrie in entries:
        print("user: " + entrie['content']['id'])
      print
      return(r.headers['EMC-CSRF-TOKEN'])

  else:
      print(r.status_code)
      print("Failed to get request")
      print
      
def yes_no_input(NEW_USER):
    while True:
        choice = raw_input("Do you want to create user " + NEW_USER + "? [y/n]").lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

def createUser():

  NEW_USER = raw_input('Please Unity\'s new user name: ')
  print('Default password is "Passw0rd!".')
  print

  HEADERS2 = {'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-EMC-REST-CLIENT': 'true',
              'EMC-CSRF-TOKEN': token }
 
  BODY = {"name": NEW_USER,
          "role": "operator",
          "password": "Passw0rd!"}

  if yes_no_input(NEW_USER):
      r2 = s.post(URL, headers = HEADERS2, data = json.dumps(BODY), verify=False)
      if r2.status_code == 201:
          print('Successed to create user request')
          print(r2.status_code)
          print
#          print(r2.headers)
      else:
          print(r2.status_code)
          print("Failed to post request")
          print


if __name__ == '__main__':
  token = printUsers()
  if token:
    createUser()
    printUsers()

  s.close()
