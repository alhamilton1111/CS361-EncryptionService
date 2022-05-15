import time
import requests
from datetime import datetime

######################################################
# Encryption FUNCTIONS
######################################################
######################################################
# This function generates the key in a cyclic manner until
# it's length isn't equal to the length of original text
######################################################
def generateKey(size, keyIn):
    key = list(keyIn)
    if size == len(key):
        return key
    else:
        for i in range(size - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


######################################################
# encrypted text generated with the help of the key
######################################################
def cipherText2(string1, string2, key):
    # print(f"{string1}<name pw>{string2}")
    cipher_text = []
    cipher_text2 = []
    for i in range(len(string1)):
        # print(f"CHAR: {string[i]} Offset: {key[i]%26} CypherCHAR: {x}")
        rawX = (ord(string1[i]) + ord(key[i])) % 26
        x = rawX + ord('A')
        cipher_text.append(chr(x))
        #                   N       78      f       24      24      89      Y
        #       89 + 24 = 113 - 97
        #                   o       111     r       10      17      82      R

        # print(f"CHAR: {string[i]} ORD: {ord(string[i])} KEY: {key[i]} Offset: {ord(key[i]) % 26} CypherCHAR: {rawX} FINAL Value: {x} FinalCHAR: {chr(x)}")
    for i in range(len(string2)):
        # print(f"CHAR: {string[i]} Offset: {key[i]%26} CypherCHAR: {x}")
        rawX2 = (ord(string2[i]) +
                 ord(key[i])) % 26
        x2 = rawX2 + ord('A')
        cipher_text2.append(chr(x2))
    # print(f" {cipher_text} {cipher_text2}")
    return "".join(cipher_text), "".join(cipher_text2)


def cipherText1(string1, key):
    # print(f"{string1}<name pw>{string2}")
    cipher_text = []
    for i in range(len(string1)):
        # print(f"CHAR: {string[i]} Offset: {key[i]%26} CypherCHAR: {x}")
        rawX = (ord(string1[i]) + ord(key[i])) % 26
        x = rawX + ord('A')
        cipher_text.append(chr(x))
        #                   N       78      f       24      24      89      Y
        #       89 + 24 = 113 - 97
        #                   o       111     r       10      17      82      R

        # print(f"CHAR: {string[i]} ORD: {ord(string[i])} KEY: {key[i]} Offset: {ord(key[i]) % 26} CypherCHAR: {rawX} FINAL Value: {x} FinalCHAR: {chr(x)}")
    # print(f" {cipher_text} {cipher_text2}")
    return "".join(cipher_text)


######################################################
# Start Service FUNCTIONS
######################################################
def startServices(keyword):
    #####################################################
    # Build System Encryption Key to become a microService
    # keyword = "scuba"
    stringIn = 'myuseridandmyassociatedpasswordwithsomeextra'  # ??????????? ID + PW Length
    sysKey = generateKey(len(stringIn), keyword)
    #####################################################
    print("# Displayed for testing purposes #")
    with open("malUsers.txt", "w") as malFile:
        print("creating Malicious Users File...")
        malUser1 = "fred"
        cipher_text1 = cipherText1(malUser1, sysKey)
        # print("Ciphertext :", cipher_text1)
        malFile.write(f"{cipher_text1}\n")
    malFile.close()
    showMalUsers()

    with open("validUsers.txt", "w") as pwFile:
        print("creating PW File...")
        addUser("dave", "123", sysKey)
        addUser("andrea", "4567", sysKey)
        addUser("fred", "12345", sysKey)
    showUsers()

    #!!!
    # setup Elizabeth's Help MicroService
    with open("helpMe.txt", "w") as helpFile:
        helpFile.write("help")
        helpFile.close()

    return sysKey


def addUser(userid, pw, key):
    with open("validUsers.txt", "a") as pwFile:
        print(f"Adding User: {userid} to system ...")
        #
        userC, passwordC = cipherText2(userid, pw, key)
        # print("Ciphertext :", cipher_text1)
        pwFile.write(f"{userC:<12} {passwordC:<12}  => {userid:<12}\n")
    pwFile.close()


######################################################
# HELP and User Interface FUNCTIONS
######################################################
def introduction():
    textoutput = '''
    This encryption System enables a user to enter free from txt or provide a file name
    where their text to encrypt may be found and will return an encrypted version of that text
    for them to share with other users.
    '''
    return textoutput


def welcomeSumry():
    welcome = '''### AH Enterprises all rights reserved ###
    \n    Glad you have chosen to use this Encryption / Decryption 
    microservice, provided by AHE.\n
    It is an Encryption and Decryption service for users that are authorized to
    use the system. And it is based on the Vigenere Encryption Methodology.

    If at anytime you have a question on how to use this system, please type "help" 
    at any prompt and you will be directed to some guidance on how to proceed.
    '''
    return welcome

def helpHelp(actionReq):
    print("in help: ", actionReq)
    helpSegments = {"encrypt": "Help for Encryption is to follow:...",
                    "decrypt": "Help for Decryption is to follow...",
                    "intro": welcomeSumry(),
                    "overview": introduction(),
                    "login": " You must enter a valid userID/PW for an active account..."
                             "\nRemember 'help' is not a valid UserId or Password "
                             "\nPlease try again."}
    return helpSegments[actionReq]


######################################################
# System Navigation to Services FUNCTIONS
######################################################
def actionToTake(userReq, key, systemWord):
    sources = ['file', 'prompt']
    write_help()
    if userReq.lower() == 'help':
        print("...Help is coming from Elizabeth's MicroService!")
        # call to help microservice
        # using Elizabeth's Help MicroService
        time.sleep(1)
        print(get_help())


    elif userReq.lower() == "encrypt":
        source = input(f"What will be the source of your text to encrypt? {sources} ")
        userText = ""
        if source == 'file':
            fileIn = input(f"looking for a local file:...? ")
            with open(fileIn, "r") as inFile:
                userText = inFile.read()

        elif source == 'prompt':
            userText = input("We will start the Encryption as soon as you either hit enter... ")
        print(f"\n\t\t...Encrypting!     A Text Length of: {len(userText)}")
        # Encrypt User Data from File or Input Prompt
        fileKey = generateKey(len(userText), systemWord)
        print("FILE KEY LEN:", len(fileKey))
        encrytpedText = cipherText1(userText, fileKey)
        print("Encrypted")
        # Display Encrypted Results
        showEncryption(encrytpedText)

        # call encrypt microservice
    elif userReq.lower() == "decrypt":
        print("...Decrypting! \n \t\t\tUnder Construction")
        # call decrypt microservice
    elif userReq.lower() == "overview" or userReq.lower() == "intro":
        print(helpHelp(userReq))
    elif userReq.lower() == "login":
        login()
    else:
        print("Have a Nice Day! More HELP is Planned. Stay tuned.")
        # call goodbye microservice to close all services


def getUserReq(goodActions):
    req = input(f"How can we Help today? {goodActions} ")
    while req not in goodActions:
        req = input(f"Please use a keyword for us to better assist you today? {goodActions} ")
    return req


######################################################
# Print for Debug FUNCTIONS
######################################################
def showEncryption(textIn):
    sizeIn = len(textIn)
    lineSize = 60
    start = 0
    stop = lineSize
    while sizeIn > lineSize:
        print(textIn[start:stop])
        start += lineSize
        stop += lineSize
        sizeIn -= lineSize
    print(textIn[start:])


###########################################################
# 2 show functions to read and print file contents
###########################################################
def showUsers():
    print("# Displayed for testing purposes # \nEncypted Users...")
    with open("validUsers.txt", "r") as pwFileRead:
        print(pwFileRead.read())


def showMalUsers():
    print("# Displayed for testing purposes # \nMalicious Users...")
    with open("malUsers.txt", "r") as malFileRead:
        print(malFileRead.read())


###########################################################
# Use Other Micro Services:
#           Help from Elizabeth
#           Age Verification from Joe
###########################################################
## !!
# Elizabeth's MicroService contract functions
def write_help():
    with open("helpMe.txt", "w") as f:
        f.write("help")

## !!
def get_help():
    with open("helpMe.txt") as f:
        helpful_message = f.readline()
    return helpful_message


# call to Joe's MicroService web sourced
def ageVerify(bDay):
    # val = input("Please enter a birthdate (YYYY-MM-DD): ")
    val = bDay
    access = "None"
    try:
        r = requests.get('https://api.maurer.gg/verify_age/' + val)
        if r.status_code == 200:
            data = r.json()
            if data['verified']:
                access = "full"
                #print("User is over 13.")
            else:
                access = "limited"
                #print("User is not over 13.")
        else:
            access = f"Age Verify Error: {r.status_code}"
            #print("The server returned error Status Code" + str(r.status_code))
    except:
            print("Age Verify not Working! ")

    finally:
        return access

# https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
def validate(dateIn):
    try:
        if dateIn != datetime.strptime(dateIn, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


# Use Joe Age Verification Service
def verifyAge(userId):
    result = ""
    birthday = input("Please enter a birthdate (YYYY-MM-DD): ")
    while not validate(birthday):
        birthday = input("Please enter a birthdate (YYYY-MM-DD): ")
    result = ageVerify(birthday)
    if result == "full":
        print(f"{userId} you have full access to our Encryption Services! ")
    elif result == "limited":
        print(f"Due to your Age,\n {userId} you have limited access to our Encryption Services! ")
    else:
        print(f"{userId}, we are sorry but there was a problem verifying your age.")
        print(f"Access will be limited for you, {userId}")




###########################################################
# Use own User ID/PW Encrypted Verification Micro Service
# Also includes Age Verification Micro Service CALL
###########################################################
def login():
    pwInvalid = True
    userId = ""
    while pwInvalid:
        userId = input("User ID: ")
        while userId == "help":
            helpHelp("login")
            userId = input("Enter a valid User ID: ")

        passWrd = input("Password: ")
        while passWrd == "help":
            helpHelp("login")
            passWrd = input("Enter a valid password: ")
        ######################################################
        # Check to see if Micro Service is ready("waiting...")
        ######################################################
        with open("loginUser.txt", "r") as userLoggingIn:
            user = userLoggingIn.read().split(" ")

            #print(f"in Read....   {user}")
            while user[0] != "waiting...":
                time.sleep(1)
                user = userLoggingIn.read().split()
                #print(user)

        userLoggingIn.close()
        outstring = userId + " " + passWrd
        # print(outstring)# Used for testing
        ######################################################
        # write UserID and UserPW into the login file to launch the MicroService Action
        ######################################################
        with open("loginUser.txt", "w") as loger:
            loger.write(outstring)
            loger.close()
        ######################################################
        # read the MicroService Communication file to see results of Login Attempt
        ######################################################
        time.sleep(1)
        with open("validUserResponse.txt", "r") as errorCheck:
            errorMsg = errorCheck.read().split(" ")
            if errorMsg[0] == userId:
                verifyAge(userId)
                print(f"Welcome {userId}, you are now logged in!")
                pwInvalid = False
            elif errorMsg[0] == "Invalid":
                print(f"Sorry that Password is invalid, Please try again.")
            else:
                verifyAge(userId)
                print(f" ...Welcome New User: {userId}")
                pwInvalid = False
            errorCheck.close()
    # End of Encryption for UserID / PW
    return userId


def welcomePage():
    welcome = '''### AH Enterprises all rights reserved ###
    \n    Glad you have chosen to use this Encryption / Decryption 
    microservice, provided by AHE.\n
    It is an Encryption and Decryption service for users that are authorized to
    use the system. And it is based on the Vigenere Encryption Methodology.
    
    If at anytime you have a question on how to use this system, please type "help" 
    at any prompt and you will be directed to some guidance on how to proceed.
    '''
    menu = '''
        1. Login
        2. Help
        '''

    print(f"{welcome}")

    print(f"{menu}")
    choice = int(input("Choice: "))
    while choice not in [1, 2]:
        choice = int(input("Please enter a valid Choice: "))

    return choice

def main():
    ############################
    # System Initialization Values
    ############################
    validActions = ['login', 'done', 'help', 'intro', 'overview', 'encrypt', 'decrypt']
    systemBaseText = "scuba"
    systemKey = startServices(systemBaseText) # Need to startup Service
    #systemKey = systemBaseText # commented out, since line above is in play

    # Begin User Interaction
    userchoice = welcomePage()
    user = ""
    while userchoice == 2:
        # userchoice = helpHelp("intro")
        userchoice = welcomePage()

    if userchoice == 1:
        user = login()
        #print(f"USER After Login: {user}")
        done = False
        while not done:

            action = getUserReq(validActions)
            while action not in validActions:
                action = getUserReq(validActions)
                helpHelp("overview")
            if action.lower() != 'done':
                actionToTake(action, systemKey, systemBaseText)
            else:
                # sendEmail() # need to debug password problem
                print(f"Logging off ==> !!! {user} !!! <==")
                print("Thanks for using the system")
                done = True


main()
