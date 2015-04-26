from getpass import getpass
from optparse import OptionParser
import requests, sys, urllib

url = "http://localhost:8000/"
commands = ["quit", "list", "get", "help"]

def log_error(error):
    f = open('error.html', 'w')
    f.write(error)
    f.close()

def authenticate(username, password):
    auth_url = url + "api/authenticate/"
    user = {'username': username, 'password': password}
    r = requests.post(auth_url, data=user)

    if r.status_code == 200:
        return r.json()["session"]

    return None

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
    report += "Location: " + json_report['location']

    return report

def list(username, token):
    reports = get_reports(username, token)

    for i, report in enumerate(reports):
        print("Report ID:", report['pk'], "(" + report['fields']['short_description'] + ")")

def help():
    print("The commands are:")
    print("\thelp - prints this page")
    print("\tlist - lists all of your reports")
    print("\tget {report_id} - gets the information for a specific report")
    print("\tdownload - downloads one of your files")

def download_files(username, token, report):
    user = {'username': username, 'token': token}
    r = requests.post(url + "api/files/" + str(report) + "/", data=user)

    if r.status_code == 200:
        for file in r.json():
            try:
                urllib.request.urlretrieve(url + "api/download/" + str(file["pk"]), file["fields"]["title"])
                print("Downloaded " + file["fields"]["title"])
            except urllib.error.HTTPError:
                r = requests.post(url + "api/download/" + str(file["pk"]) + "/", data=user)
                log_error(r.text)
    else:
        log_error(r.text)


def get(username, token, report):
    user = {'username': username, 'token': token}
    r = requests.post(url + "api/report/" + report + "/", data=user)

    if r.status_code == 200:
        report = r.json()

        download = ""
        while download != "y" and download != "n":
            download = input("Would you like to download the files (y/n): ")

        if download == 'y':
            download_files(username, token, report[0]["pk"])

        print(format_report(report[0]["fields"]))
    else:
        log_error(r.text)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username",
        help="Enter your SecureWitness username")

    (options, args) = parser.parse_args()

    username = ""
    if options.username != None:
        username = options.username
    else:
        username = input("Enter SecureWitness username: ")

    password = getpass("Enter SecureWitness password: ")
    token = authenticate(username, password)

    if token == None:
        print("Something went wrong while authenticating")
        sys.exit()

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
            elif(command[0] == "get"):
                get(username, token, command[1])
        else:
            print("Please enter a valid command. \
                Type 'help' for a list of commands")
