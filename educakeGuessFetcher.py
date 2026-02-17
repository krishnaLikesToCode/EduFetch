from curl_cffi import requests

loginSession=requests.Session(impersonate="chrome120")

username="krishnab0009"
password="bedwarrior10"

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

loginPayload={"username" : username, "password" : password, "lastname" : "", "userType" : "student","allowEmailForUsername" : True}


def getTokens(loginPayload,verbose=False):
    global loginHeaders,loginSession
    
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




# getting URL to get questionIDs from
browserUrl=("https://my.educake.co.uk/my-educake/quiz/185054455")
splitURL=browserUrl.split("/");quizID=splitURL[-1]
urlToGoTo=f"https://my.educake.co.uk/api/student/quiz/{quizID}"


# Defining security tokens for request headers
tokens=getTokens(loginPayload)

XSRF_TOKEN=tokens[0]

JWT_TOKEN=tokens[1]


# updating headers with JWT-TOKEN
headers['Authorization']= JWT_TOKEN

# gets URL reponse to request
urlResponse=loginSession.get(urlToGoTo,headers=headers)


print(f"Got question IDs with code{urlResponse.status_code}, reason {urlResponse.reason}")#give code (200 means success, 403 means JWT is probably expired, 404 is invalid quiz)


#Records text of URL
responseAsText=urlResponse.text


#sets start and end of where to look (starts at 'questions', finishes at end of questionIDs list)
start = responseAsText.find("\"questions\":[")
end = responseAsText.find(",\"questionMap\"")

#puts into iterable list format
questionIDs=((responseAsText[start:end]).replace("\"questions\":[","")).split(",")#gets questionIDs in list form, yay!

#Getting answers, using questionIDs

baseAnswerURL="https://my.educake.co.uk/api/course/question/"

correctAnswerLUT={}
correctAnswerArr=[]

for i in range(len(questionIDs)):
    answerURL=f"{baseAnswerURL}{questionIDs[i]}/mark"

    sendPrompt={"givenAnswer" : "-1"}

    answerURLresponse=loginSession.post(answerURL,headers=headers,json=sendPrompt)
    answerResponseAsText=answerURLresponse.text


    nstart=answerResponseAsText.find("\"correctAnswers\":[")

    nend=answerResponseAsText.find("],\"reasoning\":")

    correctAnswers=((answerResponseAsText[nstart:nend]).replace("\"correctAnswers\":[","")).replace("\"","").split(",")
    print(f"Question {i+1} answer: {correctAnswers}")

    

    



    


