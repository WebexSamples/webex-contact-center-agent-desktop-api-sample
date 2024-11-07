# Webex CC RESTful API Agent Desktop STARTER

This repository contains a sample Flask application that demonstrates how to integrate with the Webex Contact Center REST API. The application allows agents to log in and log out of a Desktop Session, and handles OAuth authentication with Webex.

## Prerequisites

- Python 3.6 or higher
- Flask
- Requests

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/webex-contact-center-integration.git
    cd webex-contact-center-integration
    ```

2. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

    If `requirements.txt` does not exist, you can manually install the dependencies:

    ```sh
    pip install flask requests
    ```
## Webex Contact Center Developer Sandbox or Account
    you can request a WxCC Developer Sandbox [here](https://developer.webex-cx.com/sandbox).

## Webex Contact Integration
    you will need to register a Webex Contact Center integration with cjp:user scope
    in order to get Client ID, Client Secret, Redirect, and optional Authorizaiton URL
    for OAuth 2.0 Flow.
    Learn more [here](https://developer.webex-cx.com/documentation/integrations).

## Configuration

1. **Set up variables on desktop.py:**

    add valid values to the following variables:

    ```
    CLIENT_ID=YourClientId
    CLIENT_SECRET=YourClientSecret
    REDIRECT_URI=http://0.0.0.0:10060/oauth
    AGENT_ID=YourAgentId
    TEAM_ID=YourTeamId
    DIAL_NUMBER=1001
    ```

2. **Add Auth URL on index.html:**
    ```
    <a href='Your Authorization url here'>
    ```

## Running the Application

1. **Start the Flask application:**

    ```sh
    python3 desktop.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:10060`.

## Usage

- **Authorize:** Click the "Grant" button on the main page to start the OAuth process and log in as an agent. Please use a user with the roles of AGENT as the roles parameter in the body of the
api call was hardcoded.
- **Agent Login:** Click the "Login" button on the granted.html page to log in to a WxCC Desktop Session.
- **Agent Logout:** Click the "Logout" button on the agent_loggedin.html page to log out of the WxCC Desktop Session.

## Functions

- **agentLogout:** Logs out the agent from the Webex Contact Center.
- **agentLogin:** Logs in the agent to the Webex Contact Center.
- **get_tokens:** Retrieves access and refresh tokens using the authorization code.
- **get_tokens_refresh:** Refreshes the access token using the refresh token.
- **main_page:** Renders the main page with the "Grant" button.
- **oauth:** Handles the OAuth redirect and retrieves the authorization code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy coding! 🚀