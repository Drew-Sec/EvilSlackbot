#! /usr/bin/env python3

import os
from slack import WebClient
import argparse

def div():
    print('------------------------------------------')
parse = argparse.ArgumentParser()
# Display help 
parse.add_argument('-t','--token',help='Slack Oauth token',action='store')
parse.add_argument('-e','--email',help='Email of target',action='store')
parse.add_argument('-eL','--email_list',help='Path to list of emails separated by newline',action='store')
parse.parse_args()
args = parse.parse_args()

t = WebClient(args.token)
user_id = ""
# lookup userid by email address
def lookupByEmail():
    lookup = t.api_call("users.lookupByEmail?email=" + args.email)
    #print(lookup['user']['id'])
    global user_id
    user_id = lookup['user']['id']
botname,icon,message = '','',''
def setupMessage():
    global botname,icon,message
    div()
    botname = input('Type the name you\'d like to impersionate\nExample: SecurityBot\n')
    div()
    icon = input('Type the URL to an image you\'d like to use as your profile photo\n')
    div()
    message = input('Type your slack message\nExample: You have been mentioned in <https://google.com|Doc-3972>\n')
    div()
    print('Spoofed name is: ' + botname + '\n'
          'Icon URL: ' + icon + '\n'
          'Slack Message: ' + message + '\n'
        )
    div()
    ready = input('Ready to send your message? y/n\n')
    if ready != 'y':
        exit()
    elif args.email_list != None:
        sendMessageToList()
    else:
        lookupByEmail()
        sendMessage()
def sendMessage():
    send = t.chat_postMessage(
        channel=user_id,
        username=botname,
        icon_url=icon,
        text=message
        )

def sendMessageToList():
    r = open(args.email_list)
    for address in r.readlines():
        lookupByEmailList(address)
        sendMessage()
        print("Sending Message to: " + address)
    r.close()
def lookupByEmailList(email_address):
    lookup = t.api_call("users.lookupByEmail?email=" + email_address)
    #print(lookup['user']['id'])
    global user_id
    user_id = lookup['user']['id']    
setupMessage()
