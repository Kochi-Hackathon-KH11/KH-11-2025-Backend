# Kochi Hackathon 2025 Backend — DAMN.ai (KH11)
## Overview
This repository contains the backend codebase for the DAMN.ai project, developed during the Kochi Hackathon 2025 (KH11). The backend is built using Python and includes functionalities for audio processing, user management, and utility services.

## Features
- Audio Processing: Manage and process audio data efficiently.
- User Management: Handle user authentication and profiles.
- Utility Services: Provide auxiliary functions to support core features.


## Project Structure: The repository is organized as follows:
- `audio/`: Audio processing and streaming functionalities.
- `user/`: Handles user authentication and other user related .
- `utils/`: Utility functions to communicate with the AI models.
- `kh11backend/`: Main backend application directory.
- `Dockerfile`: Instructions to build the Docker image for the application.
- `socket-server.py`: WebSocket server to facilitate handshaking between clients to initiate WebRTC connection.


## Getting Started
###  Prerequisites
- Python 3.8 or higher
- Docker (optional, for containerized deployment)


### Installation
#### Clone the repository:

```bash
Copy
Edit
git clone https://github.com/Kochi-Hackathon-KH11/KH-11-2025-Backend.git
cd KH-11-2025-Backend
```
#### Create and activate a virtual environment:

```bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

#### Install dependencies:
```bash
Copy
Edit
pip install -r requirements.txt
```
### Running the Application
#### Apply database migrations:
```bash
Copy
Edit
python manage.py migrate
```

#### Start the development server:
```bash
Copy
Edit
python manage.py runserver
```
The application will be accessible at http://127.0.0.1:8000/.

