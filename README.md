# Cyoda-AI

Cyoda-AI is an application that provides configuration and code necessary to generate app-specific resources for your Cyoda environment. This application interacts with Cyoda's API and gRPC services using secure credentials and a predefined workspace directory.

## Prerequisites
Before using this application, make sure you have the following installed:

Python 3.x
Required Python dependencies (specified in requirements.txt)
Access to a Cyoda environment (API key, secret, and URL)

### Setup

Clone the repository:
```
git clone https://github.com/your_username/cyoda-ai.git
cd cyoda-ai
```

Install dependencies:

Use pip or a virtual environment to install the required dependencies listed in requirements.txt:

```
pip install -r requirements.txt
```

Set up environment variables:

Create a .env file in the root directory and configure it with the following values:

```
WORK_DIR="/workspaces/cyoda-ai"
CYODA_API_KEY=your_user
CYODA_API_SECRET=your_password
CYODA_API_URL=https://your_env.cyoda.net
GRPC_ADDRESS=grpc-your_env.cyoda.net
```