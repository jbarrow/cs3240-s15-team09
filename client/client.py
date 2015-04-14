from getpass import getpass
from optparse import OptionParser

url = "http://localhost:8000/"

def authenticate(username, password):
    auth_url = url + "api/authenticate"
    

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", help="Enter your SecureWitness username")

    (options, args) = parser.parse_args()

    if options.username != None:
        user = options.username
    else:
        input("Enter SecureWitness username: ")

    password = getpass("Enter SecureWitness password: ")

    authenticate(username, password)
