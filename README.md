# Webex Contact Center Agent Desktop API Sample

A comprehensive Flask application demonstrating how to integrate with the Webex Contact Center REST API. This sample showcases agent desktop session management, OAuth authentication, and seamless integration with Webex Contact Center services.

## 🎯 Features

This sample shows how to use the Webex Contact Center API to do the following:

* **OAuth Authentication** with Webex Contact Center
* **Agent Login** to desktop sessions programmatically  
* **Agent Logout** from desktop sessions
* **Token Management** with automatic refresh handling
* **Session Management** with Flask session storage
* **Error Handling** with retry logic for expired tokens

## 📚 Prerequisites

### Software Requirements

- **Python 3.6 or higher**
- **Flask** web framework
- **Requests** library for HTTP calls

### Webex Contact Center Requirements

- **Webex Contact Center Account** or [Developer Sandbox](https://developer.webex-cx.com/sandbox)
- **Webex Contact Center Integration** with `cjp:user` scope
- **Agent ID** and **Team ID** from your Contact Center configuration
- **Dial Number** for agent extension

## 🚀 Quick Start

### Getting Your Integration Credentials

1. **Request Developer Sandbox**: Visit [developer.webex-cx.com/sandbox](https://developer.webex-cx.com/sandbox)
2. **Register Integration**: Create a Webex Contact Center integration with `cjp:user` scope
3. **Learn More**: [Integration Documentation](https://developer.webex-cx.com/documentation/integrations)
4. **Gather Required Information**:
   - Client ID and Client Secret
   - Agent ID (from Control Hub or WebSocket notifications)
   - Team ID (from Control Hub or WebSocket notifications)
   - Dial Number for agent

### Setup Instructions

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-repo/webex-contact-center-integration.git
   cd webex-contact-center-integration
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   Or install manually:

   ```sh
   pip install flask requests
   ```

3. **Configure variables in `desktop.py`:**

   ```python
   CLIENT_ID = "YourClientId"
   CLIENT_SECRET = "YourClientSecret"
   REDIRECT_URI = "http://0.0.0.0:10060/oauth"
   AGENT_ID = "YourAgentId"
   TEAM_ID = "YourTeamId"
   DIAL_NUMBER = "1001"
   ```

4. **Add Authorization URL in `templates/index.html`:**

   ```html
   <a href='Your Authorization URL here'>
   ```

5. **Start the application:**

   ```sh
   python3 desktop.py
   ```

6. **Access the application:**

   Open your browser and navigate to `http://127.0.0.1:10060`

## 📁 Project Structure

```
webex-contact-center-agent-desktop-api-sample/
├── desktop.py              # Main Flask application
├── requirements.txt        # Python dependencies
├── static/css/            # CSS styling files
├── templates/             # HTML templates
│   ├── index.html         # Main authorization page
│   ├── granted.html       # Post-authorization page
│   ├── agent_loggedin.html # Agent logged in state
│   └── temp.html          # Base template
├── package.json           # Development tools configuration
└── README.md              # This file
```

## 🔧 Functionality Overview

### Core Features

| Feature | Description | API Endpoint |
|---------|-------------|--------------|
| **OAuth Flow** | Authenticate with Webex Contact Center | `/v1/access_token` |
| **Agent Login** | Start agent desktop session | `/v1/agents/login` |
| **Agent Logout** | End agent desktop session | `/v1/agents/logout` |
| **Token Refresh** | Automatically refresh expired tokens | `/v1/access_token` |

### Application Flow

1. **Authorization**: Agent clicks "Connect to WxCC" to start OAuth flow
2. **Token Exchange**: Authorization code exchanged for access and refresh tokens
3. **Agent Login**: Agent clicks "Agent Login" to start desktop session
4. **Session Active**: Agent can handle calls and perform contact center functions
5. **Agent Logout**: Agent clicks "Agent Logout" to end desktop session

## 🔐 Authentication & Authorization

### OAuth 2.0 Flow

The application implements the standard OAuth 2.0 authorization code flow:

```python
# Token exchange
def get_tokens(code):
    url = "https://webexapis.com/v1/access_token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    # Exchange code for tokens
```

### Token Management

The application includes automatic token refresh:

```python
def get_tokens_refresh():
    # Refresh expired access tokens using refresh token
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": session['refresh_token']
    }
```

## 📡 API Integration

### Agent Login

```python
@app.route("/agentlogin", methods=['POST'])
def agentLogin():
    url = "https://api.wxcc-us1.cisco.com/v1/agents/login"
    payload = {
        "dialNumber": dialNumber,
        "teamId": teamId,
        "isExtension": True,
        "roles": ["agent"],
        "deviceType": "BROWSER"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
```

### Agent Logout

```python
@app.route("/agentlogout", methods=['POST'])
def agentLogout():
    url = "https://api.wxcc-us1.cisco.com/v1/agents/logout"
    payload = {
        "logoutReason": "AGENT_LOGOUT from sample app",
        "agentId": agentId
    }
```

### Error Handling

The application includes comprehensive error handling with automatic retry:

```python
if response.status_code != 202:
    if response.status_code == 401:
        get_tokens_refresh()  # Refresh token and retry
        response = requests.request("POST", url, json=payload, headers=headers)
```

## 🎨 User Interface

The application uses a clean, minimal web interface with:

- **Bootstrap-style CSS** for professional appearance
- **Flask templates** with inheritance for maintainable code
- **Form-based interactions** for agent login/logout
- **Responsive design** that works on desktop and mobile

### Page Flow

1. **index.html**: Main page with "Connect to WxCC" button
2. **granted.html**: Post-authorization page with "Agent Login" button
3. **agent_loggedin.html**: Active session page with "Agent Logout" button

## 🔧 Configuration Details

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CLIENT_ID` | Integration Client ID | `C1234567890abcdef...` |
| `CLIENT_SECRET` | Integration Client Secret | `secret123...` |
| `REDIRECT_URI` | OAuth redirect URL | `http://0.0.0.0:10060/oauth` |
| `AGENT_ID` | Contact Center Agent ID | `agent123@example.com` |
| `TEAM_ID` | Contact Center Team ID | `team456` |
| `DIAL_NUMBER` | Agent extension number | `1001` |

### Finding Agent and Team IDs

You can obtain Agent ID and Team ID through:

1. **Control Hub**: Webex Contact Center administration portal
2. **WebSocket Notifications**: [Subscribe to notifications](https://developer.webex-cx.com/documentation/notification/v1/subscribe-notification)
3. **API Calls**: Use Contact Center APIs to retrieve user and team information

## 🌐 Production Considerations

### Security Best Practices

1. **Environment Variables**: Store credentials in environment variables, not source code
2. **HTTPS**: Use HTTPS in production for secure token transmission
3. **Token Storage**: Implement secure token storage (not Flask sessions)
4. **Rate Limiting**: Implement API rate limiting and retry logic

### Deployment

For production deployment:

```python
# Use environment variables
import os
CLIENT_ID = os.getenv('WXCC_CLIENT_ID')
CLIENT_SECRET = os.getenv('WXCC_CLIENT_SECRET')
AGENT_ID = os.getenv('WXCC_AGENT_ID')
```

### Error Handling

```python
# Enhanced error handling for production
try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"API call failed: {e}")
    # Implement retry logic or user notification
```

## 🔧 Development

### Local Development

1. **Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Debug Mode**:
   ```python
   if __name__ == '__main__':
       app.run("0.0.0.0", port=10060, debug=True)
   ```

### Adding Features

Example: Adding agent state management:

```python
@app.route("/agentstatus", methods=['GET'])
def agentStatus():
    url = "https://api.wxcc-us1.cisco.com/v1/agents/status"
    headers = {"Authorization": f"Bearer {session['oauth_token']}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

## 🔗 Related Resources

- [Webex Contact Center Developer Portal](https://developer.webex-cx.com/)
- [Contact Center API Documentation](https://developer.webex-cx.com/documentation/rest-api)
- [Integration Management](https://developer.webex-cx.com/documentation/integrations)
- [Developer Sandbox Request](https://developer.webex-cx.com/sandbox)
- [WebSocket Notifications](https://developer.webex-cx.com/documentation/notification)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with Contact Center environment
5. Submit a pull request

## 📄 License

This project is licensed under the **Cisco Sample Code License**.

### License Summary

- ✅ **Permitted**: Copy, modify, and redistribute for use with Cisco products
- ❌ **Prohibited**: Use independent of Cisco products or to compete with Cisco
- ℹ️ **Warranty**: Provided "as is" without warranty
- ℹ️ **Support**: Not supported by Cisco TAC

See the [LICENSE](LICENSE) file for full license terms.

## 🆘 Support

- Create an issue in this repository
- Visit [Webex Contact Center Developer Support](https://developer.webex-cx.com/support)
- Join the [Webex Developer Community](https://developer.webex.com/community)

---

**Ready to integrate with Webex Contact Center!** 🚀
