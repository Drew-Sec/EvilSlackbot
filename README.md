![EvilSlackbot](https://raw.githubusercontent.com/Drew-Sec/EvilSlackbot/drewsec/images/logo.png)
# EvilSlackbot
A Slack Attack Framework for conducting Red Team and phishing exercises within Slack workspaces. 

## Disclaimer 
This tool is intended for Security Professionals only. Do not use this tool against any Slack workspace without explicit permission to test. Use at your own risk.

## Background
Millions of organizations utilize Slack to help their employees communicate, collaborate, and interact. Many of these Slack workspaces install apps or bots that can be used to automate different tasks within Slack. These bots are individually provided permissions that dictate what tasks the bot is permitted to request via the Slack API. To authenticate to the Slack API, each bot is assigned an api token that begins with **xoxb** or **xoxp**. More often than not, these tokens are leaked somewhere. When these tokens are exfiltrated during a Red Team exercise, it can be a pain to properly utilize them. Now **EvilSlackbot** is here to automate and streamline that process. **You can use **EvilSlackbot** to send spoofed Slack messages, phishing links, files, and search for secrets leaked in slack.**

## Phishing Simulations
In addition to red teaming, **EvilSlackbot** has also been developed with Slack phishing simulations in mind. To use **EvilSlackbot** to conduct a Slack phishing exercise, simply create a bot within Slack, give your bot  the permissions required for your intended test, and provide **EvilSlackbot** with a list of emails of employees you would like to test with simulated phishes (Links, files, spoofed messages) 

## Installation 
**EvilSlackbot** requires python3 and Slackclient 
```
pip3 install slackclient
```
## Usage
```
usage: EvilSlackbot.py [-h] -t TOKEN [-sP] [-m] [-s] [-a] [-f FILE] [-e EMAIL]
                       [-cH CHANNEL] [-eL EMAIL_LIST] [-c] [-o OUTFILE] [-cL]

options:
  -h, --help            show this help message and exit

Required:
  -t TOKEN, --token TOKEN
                        Slack Oauth token

Attacks:
  -sP, --spoof          Spoof a Slack message, customizing your name, icon, etc
                        (Requires -e,-eL, or -cH)
  -m, --message         Send a message as the bot associated with your token
                        (Requires -e,-eL, or -cH)
  -s, --search          Search slack for secrets with a keyword
  -a, --attach          Send a message containing a malicious attachment (Requires -f
                        and -e,-eL, or -cH)

Arguments:
  -f FILE, --file FILE  Path to file attachment
  -e EMAIL, --email EMAIL
                        Email of target
  -cH CHANNEL, --channel CHANNEL
                        Target Slack Channel (Do not include #)
  -eL EMAIL_LIST, --email_list EMAIL_LIST
                        Path to list of emails separated by newline
  -c, --check           Lookup and display the permissions and available attacks
                        associated with your provided token.
  -o OUTFILE, --outfile OUTFILE
                        Outfile to store search results
  -cL, --channel_list   List all public Slack channels
```
## Token
To use this tool, you must provide a xoxb or xoxp token. 
```
Required:
  -t TOKEN, --token TOKEN  (Slack xoxb/xoxp token)
```
```
python3 EvilSlackbot.py -t <token>
```
## Attacks
Depending on the permissions associated with your token, there are several attacks that **EvilSlackbot** can conduct. **EvilSlackbot** will automatically check what permissions your token has and will display them and any attack that you are able to perform with your given token.  
![Token Permission Check](https://raw.githubusercontent.com/Drew-Sec/EvilSlackbot/drewsec/images/check.png)

```
Attacks:
  -sP, --spoof   Spoof a Slack message, customizing your name, icon, etc (Requires -e,-eL, or -cH)

  -m, --message  Send a message as the bot associated with your token (Requires -e,-eL, or -cH)

  -s, --search   Search slack for secrets with a keyword 

  -a, --attach   Send a message containing a malicious attachment (Requires -f and -e,-eL, or -cH)
```
### __Spoofed messages (-sP)__
With the correct token permissions, **EvilSlackbot** allows you to send phishing messages while impersonating the botname and bot photo. This attack also requires either the **email address (-e)** of the target, a **list of target emails (-eL)**, or the name of a **Slack channel (-cH)**. **EvilSlackbot** will use these arguments to lookup the SlackID of the user associated with the provided emails or channel name. To automate your attack, use a list of emails.

```
python3 EvilSlackbot.py -t <xoxb token> -sP -e <email address>

python3 EvilSlackbot.py -t <xoxb token> -sP -eL <email list>

python3 EvilSlackbot.py -t <xoxb token> -sP -cH <Channel name>
```

### __Phishing Messages (-m)__
With the correct token permissions, **EvilSlackbot** allows you to send phishing messages containing phishing links. What makes this attack different from the Spoofed attack is that this method will send the message as the bot associated with your provided token. You will not be able to choose the name or image of the bot sending your phish. This attack also requires either the **email address (-e)** of the target, a **list of target emails (-eL)**, or the name of a **Slack channel (-cH)**. **EvilSlackbot** will use these arguments to lookup the SlackID of the user associated with the provided emails or channel name. To automate your attack, use a list of emails.
```
python3 EvilSlackbot.py -t <xoxb token> -m -e <email address>

python3 EvilSlackbot.py -t <xoxb token> -m -eL <email list>

python3 EvilSlackbot.py -t <xoxb token> -m -cH <Channel name>
```

### __Secret Search (-s)__
With the correct token permissions, **EvilSlackbot** allows you to search Slack for secrets via a keyword search. Right now, this attack requires a xoxp token, as xoxb tokens can not be given the proper permissions to keyword search within Slack. Use the -o argument to write the search results to an outfile. 
```
python3 EvilSlackbot.py -t <xoxp token> -s -o <outfile.txt>
```

### __Attachments (-a)__
With the correct token permissions, **EvilSlackbot** allows you to send file attachments. The attachment attack requires a **path to the file (-f)** you with to send. This attack also requires either the **email address (-e)** of the target, a **list of target emails (-eL)**, or the name of a **Slack channel (-cH)**. **EvilSlackbot** will use these arguments to lookup the SlackID of the user associated with the provided emails or channel name. To automate your attack, use a list of emails.
```
python3 EvilSlackbot.py -t <xoxb token> -a -f <path to file> -e <email address>

python3 EvilSlackbot.py -t <xoxb token> -a -f <path to file> -eL <email list>

python3 EvilSlackbot.py -t <xoxb token> -a -f <path to file> -cH <Channel name>
``` 

## Arguments
```
Arguments:
  -f FILE, --file FILE  Path to file attachment
  -e EMAIL, --email EMAIL  Email of target
  -cH CHANNEL, --channel CHANNEL  Target Slack Channel (Do not include #)
  -eL EMAIL_LIST, --email_list EMAIL_LIST  Path to list of emails separated by newline
  -c, --check   Lookup and display the permissions and available attacks associated with your provided token.
  -o OUTFILE, --outfile OUTFILE Outfile to store search results
  -cL, --channel_list   List all public Slack channels
```
### Channel Search
With the correct permissions, **EvilSlackbot** can search for and list all of the public channels within the Slack workspace. This can help with planning where to send channel messages. Use -o to write the list to an outfile. 

```
python3 EvilSlackbot.py -t <xoxb token> -cL
```