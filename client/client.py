from getpass import getpass
from optparse import OptionParser
import requests, sys

url = "http://localhost:8000/"
commands = ["quit", "list", "get", "download", "help"]

def authenticate(username, password):
    auth_url = url + "api/authenticate/"
    user = {'username': username, 'password': password}
    r = requests.post(auth_url, data=user)

    if r.status_code == 200:
        return r.json()["session"]

    print("Something went wrong while authenticating")
    sys.exit()

def get_reports(username, token):
    user = {'username': username, 'token': token}
    r = requests.post(url + "api/reports/", data=user)

    if r.status_code == 200:
        return r.json()
    else:
        f = open('output.html', 'w')
        f.write(r.text)
        f.close()
        print(r.status_code)

def format_report(json_report):
    report = "Description: " + json_report['short_description'] + "\n"
    report += "Details: " + json_report['detailed_description'] + "\n"
    report += "Location: " + json_report['location'] + "\n"

    return report

def list(username, token):
    reports = get_reports(username, token)

    for i, report in enumerate(reports):
        print("Report", i+1)
        print(format_report(report['fields']))

def help():
    print("The commands are:")
    print("\thelp - prints this page")
    print("\tlist - lists all of your reports")
    print("\tget - gets the information for a specific report")
    print("\tdownload - downloads one of your files")

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", help="Enter your SecureWitness username")

    (options, args) = parser.parse_args()

    username = ""
    if options.username != None:
        username = options.username
    else:
        input("Enter SecureWitness username: ")

    password = getpass("Enter SecureWitness password: ")
    token = authenticate(username, password)

    command = ""
    while command != "quit":
        command = input("> ")
        command = command.split()
        if command[0] in commands:
            if(command[0] == "list"):
                list(username, token)
            elif(command[0] == "help"):
                help()
            elif(command[0] == "quit"):
                sys.exit()
        else:
            print("Please enter a valid command. Type 'help' for a list of commands")
