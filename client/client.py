from getpass import getpass
from optparse import OptionParser
import requests, sys

url = "http://localhost:8000/"

def authenticate(username, password):
    auth_url = url + "api/authenticate/"
    r = requests.post(auth_url, user)

    if r.status_code == 200:
        return r.json()["session"]

    print("Something went wrong while authenticating")
    sys.exit()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", help="Enter your SecureWitness username")

    (options, args) = parser.parse_args()

    if options.username != None:
        user = options.username
    else:
        input("Enter SecureWitness username: ")

    password = getpass("Enter SecureWitness password: ")

    session = authenticate(username, password)
