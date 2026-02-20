from curl_cffi import requests
import customtkinter as tk
from customtkinter import END

uPassFromGUI,uNameFromGUI,urlFromGUI="","",""

#----------
# FRONT-END
#----------

# Root window
root=tk.CTk()
root.geometry("400x620")
root.title("EduFetch v1.0.1")

urlEntered=tk.BooleanVar(value=False)

urlEntryAndButton=tk.CTkFrame(root,width=375,fg_color="transparent")
searchQuestionEntryAndButton=tk.CTkFrame(root,width=375,fg_color="transparent")

nameLabel=tk.CTkLabel(root,width=350,height=1,corner_radius=30,text="Welcome to EduFetch",font=("default",23,"bold"))

writeLabel=tk.CTkLabel(root,width=350,height=40,text="Enter the Educake quiz URL...")
blankSpace=tk.CTkLabel(root,height=10,text="\n")
blankSpace1=tk.CTkLabel(root,height=5,text="\n")
inputEntry=tk.CTkEntry(urlEntryAndButton,width=300,corner_radius=30,border_color="purple",text_color="white",border_width=2,fg_color="gray20")
confirmButton=tk.CTkButton(urlEntryAndButton,width=75,corner_radius=30,border_color="purple",text="Confirm",fg_color="gray22",border_width=2,hover_color="purple")


searchQuestionLabel=tk.CTkLabel(searchQuestionEntryAndButton,width=300,text="No questions found. Enter a valid URL above first.")
searchQuestionEntry=tk.CTkEntry(searchQuestionEntryAndButton,width=50,height=15,corner_radius=30,border_color="purple",border_width=1)
searchAnswerLabel=tk.CTkLabel(root,width=365,corner_radius=30,border_color="purple",border_width=2,text="",fg_color="gray20")

scrollableArea=tk.CTkScrollableFrame(root,fg_color="gray20",width=365,height=350,scrollbar_button_hover_color="purple")


# Password and username prompt window


promptWindow=tk.CTkToplevel()
promptWindow.geometry("300x160")
promptWindow.title("")
credsEntered=tk.BooleanVar(value=False)

userNameSect=tk.CTkFrame(promptWindow,width=475,fg_color="transparent")
userPassSect=tk.CTkFrame(promptWindow,width=475,fg_color="transparent")

promptWriteLabel=tk.CTkLabel(promptWindow,text="Enter your username and password",font=("default",15,"bold"))
blankSpacePromptWindow=tk.CTkLabel(promptWindow,height=1,text="")
uNameLabel=tk.CTkLabel(userNameSect,text="Username")
uNameEntry=tk.CTkEntry(userNameSect,text_color="white",fg_color="gray20",border_color="purple",border_width=2,width=130)
uPassEntry=tk.CTkEntry(userPassSect,text_color="white",fg_color="gray20",border_color="purple",border_width=2,width=130)
uPassLabel=tk.CTkLabel(userPassSect,text="Password")
promptConfirmBtn=tk.CTkButton(promptWindow,fg_color="gray20",border_color="purple",border_width=2,width=50,text="Confirm",hover_color="purple")

# Prompt window packing
promptWriteLabel.pack(pady=7)
userNameSect.pack()
userPassSect.pack(pady=10)
uNameLabel.pack(side="left",padx=7)
uNameEntry.pack(side="right")
uPassLabel.pack(side="left",padx=7)
uPassEntry.pack(side="right")
promptConfirmBtn.pack()

# Root window packing
nameLabel.pack(pady=5)
writeLabel.pack()
urlEntryAndButton.pack()
inputEntry.pack(side="left",padx=3)
confirmButton.pack(side="right",padx=3)
blankSpace.pack()
scrollableArea.pack(anchor="s")
blankSpace1.pack()
searchQuestionEntryAndButton.pack()
searchQuestionLabel.pack(side="left",padx=2)
searchQuestionEntry.pack(side="right",padx=2)
searchAnswerLabel.pack(pady=5)



promptWindow.withdraw()


doNothing = lambda: None

def output(message,timeDisplayed=0):
    writeLabel.configure(text=message)
    root.after(timeDisplayed,doNothing)


def usernameAndPassPrompt():
    global uPassFromGUI, uNameFromGUI
    credsEntered.set(False)
    promptWindow.deiconify()
    root.wait_variable(credsEntered)
    print(uPassFromGUI)
    return [uNameFromGUI,uPassFromGUI]

def promptConfirmFunc():
    global uPassFromGUI, uNameFromGUI
    uNameFromGUI=uNameEntry.get()
    uPassFromGUI=uPassEntry.get()
    credsEntered.set(True)
    promptWindow.withdraw()

promptConfirmBtn.configure(command=promptConfirmFunc)

def searchForAnswer(event=None):
    number=searchQuestionEntry.get()
    global correctAnswersDict
    try:searchAnswerLabel.configure(text=correctAnswersDict[f"Q{number}"])
    except:searchAnswerLabel.configure(text="Question number could not be found...")




# --------
# BACK-END 
# --------

# Declaring session variables 

# Define payload
loginPayload={"username" : "", "password" : "", "lastname" : "", "userType" : "student","allowEmailForUsername" : True}

# Define request headers for GET and POST HTTPS requests
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://my.educake.co.uk",
    "Referer": "https://my.educake.co.uk/student-login",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-CH-UA": '"Chromium";v="120", "Google Chrome";v="120"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Linux"',
    "Connection": "keep-alive",
}

# Define dictionary that will contain correctAnswers of quiz
correctAnswersDict={}

# Create session impersonating a chrome browser request
loginSession=requests.Session(impersonate="chrome120")

# Functions

def getTokens(loginPayload,verbose=False):# Function to get session XSRF-TOKEN, get/generate JWT-TOKEN and accumulate session cookies
    global loginHeaders,loginSession
    
    #URLs
    frontEndLoginURL="https://my.educake.co.uk/student-login"
    loginURL="https://my.educake.co.uk/login"
    sessionTokenURL="https://my.educake.co.uk/session-token"

    # Step 1- Send GET to front-end login page (just used to get XSRF-TOKEN instance, could be any page, but this one has no redirects)
    frontEndLoginPageResponse=loginSession.get(frontEndLoginURL,headers=headers)#send GET request
    if verbose:print(f"Front-end page request finished with code {frontEndLoginPageResponse.status_code}, starting api-based login page request...\n\n\n")

    oXSRFTOKEN=(loginSession.cookies.get_dict())['XSRF-TOKEN']#get site cookies stored in current session, extract XSRF-TOKEN
    headers["X-XSRF-TOKEN"]=oXSRFTOKEN#Add to login headers

    # Step 2- Send POST to the real login API, by sending Educake the login details in loginPayload, and Educake will refresh XSRF-TOKEN
    # giving access/authorization to get a JWT token from my.educake.co.uk/session-token
    apiLoginPageResponse = loginSession.post(loginURL,headers=headers,json=loginPayload)# send POST request with payload/login info
    if verbose:print(f"Finished API login page response with code {apiLoginPageResponse.status_code}\n\n\n")

    XSRF_TOKEN=(apiLoginPageResponse.cookies.get_dict())['XSRF-TOKEN']# Get new XSRF-TOKEN
    headers['X-XSRF-TOKEN']= XSRF_TOKEN# Replace old XSRF-TOKEN with new, permanent one

    # Step 3- Take new XSRF-TOKEN and permissions, send GET to Educake session-token generator to create session-token (aka. JWT-TOKEN)
    sessionTokenPageResponse = loginSession.get(sessionTokenURL,headers=headers)# send GET request
    if verbose:print(f"Session token URL finished with code {sessionTokenPageResponse.status_code}")

    sessionToken=sessionTokenPageResponse.json();sessionToken=sessionToken['accessToken']# Get the sent .json file, extract JWT-TOKEN
    JWT_TOKEN=f"Bearer {sessionToken}"# Add 'Bearer' tag

    if verbose:print("TOKEN fetching is done! Moving onto answer fetching...\n\n\n")

    return [XSRF_TOKEN,JWT_TOKEN]



def getUserCredentialsAndAddToHeader(forceRewrite=False,verbose=False):# Function to get user credentials, checks validity, adds to request header and saves to file
    global loginPayload
    uName,uPass="",""
    try: # If credentials file is found, and credentials are valid, assign the credentials to the login payload
        if forceRewrite:iKnowThisIsAWeirdWayToDoThisButICantReallyBeBotheredTBH=1/0
        userCredFile=open("educakeCredentials.txt","r")
        credentials=userCredFile.read().split("\n")
        uName=credentials[0]
        uPass=credentials[1]
        loginPayload['username']=uName
        loginPayload['password']=uPass
        getTokens(loginPayload)

    except:
        print("No credentials file was found, or was invalid. Creating one now...\n\n")
        validCredentials=False
        while not(validCredentials):
            guiCreds=usernameAndPassPrompt()
            getUsername=guiCreds[0]
            getPassword=guiCreds[1]
            try: 
                loginPayload["username"]=getUsername
                loginPayload["password"]=getPassword
                getTokens(loginPayload,verbose=verbose)
                print("\n\nCredentials authorized, saving them now...")
                uName=getUsername
                uPass=getPassword
                validCredentials=True
            except KeyError:
                promptWriteLabel.configure(text="Credentials invalid, try again")

        userCredFile=open("educakeCredentials.txt","w")
        userCredFile.write(f"{uName}\n{uPass}")



def getQuizURL(browserURL):# Pretty self explanitory
    splitURL=browserURL.split("/");quizID=splitURL[-1]
    return f"https://my.educake.co.uk/api/student/quiz/{quizID}"

#----------
# FRONT-END
#----------

def rootConfirmBtn():
    global urlFromGUI
    urlFromGUI=inputEntry.get()
    urlEntered.set(value=True)
    


def getUrlFromGUI():
    global urlFromGUI
    urlEntered.set(value=False)
    output("Enter the Educake quiz URL...")
    root.wait_variable(urlEntered)
    return urlFromGUI

confirmButton.configure(command=rootConfirmBtn)

#---------
# BACK-END
#---------

def fetchQuizAnswers(verbose=False):
    global correctAnswersDict

    root.update()
    # Get username and password, add to request headers
    getUserCredentialsAndAddToHeader()

    # Defining security tokens for request headers
    tokens=getTokens(loginPayload)

    XSRF_TOKEN=tokens[0]

    JWT_TOKEN=tokens[1]

    # Updating headers with JWT-TOKEN and XSRF-TOKEN
    headers['Authorization']= JWT_TOKEN
    headers['X-XSRF-TOKEN']= XSRF_TOKEN

    # Get quiz URL
    quizBrowserURL=getUrlFromGUI()
    urlToGoTo=getQuizURL(quizBrowserURL)

    # Send GET request to questionIDs URL
    urlResponse=loginSession.get(urlToGoTo,headers=headers)


    if verbose:print(f"Got question IDs with code{urlResponse.status_code}, reason {urlResponse.reason}")

    # Records text of URL
    responseAsText=urlResponse.text


    # Sets start and end of where to look (starts at 'questions', finishes at end of questionIDs list)
    start = responseAsText.find("\"questions\":[")
    end = responseAsText.find(",\"questionMap\"")

    # Puts into iterable list format
    questionIDs=((responseAsText[start:end]).replace("\"questions\":[","")).split(",")# Gets questionIDs in list form
    
    # Defining base answer URL template
    baseAnswerURL="https://my.educake.co.uk/api/course/question/"
    
    # Adding quiz length to answer dictionary
    correctAnswersDict["length"]=len(questionIDs)
    
    # Iterating through questionsIDs and getting answers
    for i in range(len(questionIDs)):
        
        # Filling in URL with QuestionID
        answerURL=f"{baseAnswerURL}{questionIDs[i]}/mark"
        
        # Defining dummy answer to send via POST
        sendPrompt={"givenAnswer" : "-1"}

        # Send POST request to URL, with dummy answer and headers, then get text reponse from page
        answerURLresponse=loginSession.post(answerURL,headers=headers,json=sendPrompt)
        answerResponseAsText=answerURLresponse.text


        # Define start point of 'correctAnswers'
        nstart=answerResponseAsText.find("\"correctAnswers\":[")

        # Define end point of 'correctAnswers'
        nend=answerResponseAsText.find("],\"reasoning\":")

        # Extract answer
        correctAnswer=((answerResponseAsText[nstart:nend]).replace("\"correctAnswers\":[","")).replace("\"","").split(",")[0]
        
        # If answer is present (mostly prevents 1 label showing when URL is invalid), display and save it
        if correctAnswer!='':
            # Display answer, add to dictionary
            correctAnswersDict[f"Q{i+1}"]= correctAnswer
            newQuestionLabel=tk.CTkLabel(scrollableArea,width=360,text=f"Q{i+1}.) {correctAnswer.capitalize()}",anchor="w",border_color="purple",border_width=1,corner_radius=30)                      
            newQuestionLabel.pack(pady=2)
            searchQuestionLabel.configure(text=f"There are {i+1} questions in this quiz.{"".join([" " for i in range(3-len(str(i+1)))])}Search for question")
            searchQuestionEntry.bind("<KeyRelease>", searchForAnswer)
            root.update()
    
    # If it failed (in which 2 rows will be there, quiz length and failed first question), delete URL in Entry and send message to retry, recall program
    if len(correctAnswersDict)<=2:
        inputEntry.delete(0,END)
        output("Invalid URL...",timeDisplayed=3000)
        fetchQuizAnswers()
        



# Run program
fetchQuizAnswers()

# Continue GUI loop
root.mainloop()
