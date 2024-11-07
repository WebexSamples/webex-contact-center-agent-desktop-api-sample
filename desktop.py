"""                _
  __      _____| |__   _____  __
  \ \ /\ / / _ \ '_ \ / _ \ \/ /
   \ V  V /  __/ |_) |  __/>  <         @WebexDevs
    \_/\_/ \___|_.__/ \___/_/\_\

"""

# -*- coding:utf-8 -*-
import requests
import json
import os


from flask import Flask, render_template, request, session

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.urandom(24)

"""
Global Variables
agentId : The agentId of the agent that is logged in. it can be gathered
            from the control hub, or programmatically from a websocket when
            an agent logs in.
    [Subscribe](https://developer.webex-cx.com/documentation/notification/v1/subscribe-notification)
teamId : The teamId of the team that the agent is a member of. This can be
            gathered from the control hub, or programmatically from a websocket
            when an agent logs in.
dialNumber : The dialNumber of the agent that is logged in.

"""
clientID = "YourClientId"
secretID = "YourClientSecret"
redirectURI = "http://0.0.0.0:10060/oauth" #Redirect URI
agentId = "YourAgentId"
teamId = "YourTeamId"
dialNumber = "1001"

"""
Function Name : agentLogout
Description : This function is called after an agent clicks the logout
                button on the agent_loggedin.html page. The function
                will make a POST request to the Webex Contact Center API
                to let the Webex Cloud know that the agent is no longer
                consuming a session on the agent desktop.
"""
@app.route("/agentlogout", methods=['POST'])
def agentLogout():
    print("function : agentLogout()")
    url = "https://api.wxcc-us1.cisco.com/v1/agents/logout"
    access_token = session['oauth_token']

    payload = {
        "logoutReason": "AGENT_LOGOUT from sample app",
        "agentId": agentId
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response)

    if response.status_code != 202:
        if response.status_code == 401:
            get_tokens_refresh()
            response = requests.request("POST", url, json=payload,
                                        headers=headers)
            if response.status_code != 202:
                return render_template("agent_loggedin.html")
        else:
            return render_template("agentloggedin.html")

    return render_template("index.html")

"""
Function Name : agentLogin
Description : This function is called after an agent authorizes the
              integration to access thier Webex account. The function
              will make a POST request to the Webex Contact Center API
              to let the Webex Cloud know that the agent is consuming a
              session on the agent desktop.
"""
@app.route("/agentlogin", methods=['POST'])
def agentLogin():
    print("function : agentLogin()")
    url = "https://api.wxcc-us1.cisco.com/v1/agents/login"
    access_token = session['oauth_token']

    payload = {
        "dialNumber": dialNumber,
        "teamId": teamId,
        "isExtension": True,
        "roles": ["agent"],
        "deviceType": "BROWSER"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response)

    if response.status_code != 202:
        if response.status_code == 401:
            get_tokens_refresh()
            response = requests.request("POST", url, json=payload, headers=headers)
            if response.status_code != 202:
                return render_template("index.html")
        else:
            return render_template("index.html")

    return render_template("agent_loggedin.html")

"""
Function Name : get_tokens
Description : This is a utility function that takes in the
              Authorization Code as a parameter. The code
              is used to make a call to the access_token end
              point on the webex api to obtain a access token
              and a refresh token that is then stored in the
              Flask Session module for use in other parts of the app.
              NOTE: IN PRODUCTION, AUTH TOKENS WOULD NOT BE STORED IN A SESSION. 
              THIS APP WILL REQUEST A NEW TOKEN EACH TIME IT RUNS WHICH WILL NOT BE 
              ABLE TO CHECK AGAINST EXPIRED TOKENS.
"""
def get_tokens(code):
    print("function : get_tokens()")
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)

    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    session['oauth_token'] = access_token
    session['refresh_token'] = refresh_token

    print("Token stored in session : ", session['oauth_token'])
    print("Refresh Token stored in session : ", session['refresh_token'])
    return

"""
Function Name : get_tokens_refresh()
Description : This is a utility function that leverages the refresh token
              in exchange for a fresh access_token and refresh_token
              when a 401 is received when using an invalid access_token
              while making an api_call().
              NOTE: in production, auth tokens would not be stored
              in a Session. This app will request a new token each time
              it runs which will not be able to check against expired tokens.
"""
def get_tokens_refresh():
    print("function : get_token_refresh()")

    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
                    "refresh_token={2}").format(clientID, secretID, session['refresh_token'])
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)

    access_token = results["access_token"]
    refresh_token = results["refresh_token"]
    [access, ciCluster, orgId] = results["access_token"].split("_")
    print ("Access Token : ", access)
    print ("CI Cluster : ", ciCluster)
    session['oauth_token'] = access_token
    session['refresh_token'] = refresh_token
    session['orgId'] = orgId
    return

"""
Function Name : main_page
Description : when using the browser to access server at
              http://127/0.0.1:10060 this function will
              render the html file index.html. That file
              contains the button that kicks off step 1
              of the Oauth process with the click of the
              grant button
"""
@app.route("/")

def main_page():
    """Main Grant page"""
    return render_template("index.html")

"""
Function Name : oauth
Description : After the grant button is click from index.html
              and the user logs into thier Webex account, the
              are redirected here as this is the html file that
              this function renders upon successful authentication
              is granted.html. else, the user is sent back to index.html
              to try again. This function retrieves the authorization
              code and calls get_tokens() for further API calls against
              the Webex API endpoints.
"""
@app.route("/oauth") #Endpoint acting as Redirect URI.

def oauth():
    print("function : oauth()")
    """Retrieves oauth code to generate tokens for users"""
    state = request.args.get("state")
    if state == '1234abcd':
        code = request.args.get("code")
        print("OAuth code:", code)
        print("OAuth state:", state)
        get_tokens(code)
        return render_template("granted.html")
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run("0.0.0.0", port=10060, debug=False)
