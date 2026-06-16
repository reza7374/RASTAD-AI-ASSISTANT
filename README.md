# Rastad AI Assistant - MVP

An intelligent lead and support assistant that utilizes AI to understand user intent and provide relevant responses.

## 🚀 Features

*   **AI-Powered Responses:** Understands user messages and generates contextually relevant replies using an LLM.
*   **Intent & Segment Detection:** Identifies user goals (e.g., VIP inquiry, exchange registration, support request) and categorizes users (e.g., new user, VIP interest, exchange signup candidate).
*   **Internal Knowledge Base:** Answers questions based on internal documentation stored in text files.
*   **Database Integration:** Persistently stores user information and message history in PostgreSQL.
*   **Admin Endpoints:** Provides functionality to manage users and view message history.
*   **Dockerized Deployment:** Enables easy setup and execution using Docker and Docker Compose.
*   **Robust Error Handling:** Manages potential errors during message processing and LLM interactions.

## ⚙️ Tech Stack

*   **Backend:** FastAPI (Python)
*   **Database:** PostgreSQL
*   **AI/LLM:** I use mock-LLM but it is easy to just change it to Real one including API base or Local one
*   **Vector Database:** FAISS 
*   **Containerization:** Docker, Docker Compose
*   **Validation:** Pydantic

## 📋 Task Requirements (MVP)

This project was developed based on the MVP requirements for the "AI Automation Engineer / Claude Expert" task, which included:

*   **Backend:** Python + FastAPI (or similar frameworks)
*   **API Endpoint:** `POST /message` with inputs: `user_id`, `name`, `message`
*   **Response Fields:** `reply`, `intent`, `user_segment`, `needs_human_support`
*   **Database:** PostgreSQL (or SQLite) for storing users and messages.
*   **Admin Endpoints:** `GET /management/users`, `GET /management/users/{user_id}/messages`
*   **Knowledge Base:** Minimum of 3 text files.
*   **LLM Integration:** Real LLM connection or a clean mock implementation.
*   **Error Handling & Logging**
*   **Dockerfile & README**

## 🚀 Getting Started

### Prerequisites:

*   **Docker & Docker Compose:** Installed on your system. ([Install Docker](https://docs.docker.com/get-docker/))
*   **Python 3.11+** (Recommended)

### Quick Setup:

1.  **Clone the Repository:**
```bash
git clone git@github.com:reza7374/RASTAD-AI-ASSISTANT.git
cd rastad-ai-assistant
```

2. **Create .env File (Optional but Recommended)**:Create a file named .env in the project root and add any necessary API keys or configurations. For example:
```
# .env
OPENAI_API_KEY=sk-your_openai_api_key_here
# If you need to override database settings from docker-compose:
# DATABASE_URL=postgresql://user:password@host:port/dbname

```
**Note:** If you are using `docker-compose up` and have defined `DATABASE_URL` within the `docker-compose.yml` file, you typically do not need to add it here unless you intend to override it.

3. **Build and Run Containers**:Execute the following command in your terminal. This will build the Docker image for your application and launch the services defined in docker-compose.yml (including FastAPI and PostgreSQL):

```
docker compose up --build

```

*(If `docker compose` command is not found, try `docker-compose` or ensure Docker Compose is installed correctly.)*

4. **Access the Application:**

**The FastAPI application will be available at** http://localhost:8000.

**API Docs (Swagger UI):** http://localhost:8000/docs
**Admin Panel (ReDoc):** http://localhost:8000/redoc
**Sending a Message (Example with curl):**
```
curl -X POST "http://localhost:8000/message/" \
-H "Content-Type: application/json" \
-d '{
"user_id": "test_user_1",
"name": "Reza",
"message": "خدمات VIP شما چیست؟"
}'

```

**Accessing Admin Endpoints:**
**List Users:** http://localhost:8000/management/users
**User Message History (e.g., for user_id=‘test_user_1’):** http://localhost:8000/management/users/test_user_1/messages

## Knowledge Base
Internal documentation files are located in the knowledge_base directory.

## Database Schema
Database models are defined in app/db/models.py and managed via SQLAlchemy ORM. Key tables include User and Message.

## Future Development & Improvements

- **Enhance Ingestion Pipeline:** The current data ingestion process needs to be expanded to handle more complex data sources, formats, and potentially perform more sophisticated pre-processing or chunking strategies. Consider implementing robust error handling, parallel processing, and schema validation for incoming data.
- **Utilize a Real LLM:** For production-level performance and capabilities, replace any mock LLM integrations with a direct connection to a powerful, real-world Large Language Model (e.g., OpenAI’s GPT series, Anthropic’s Claude, or other state-of-the-art models). This will unlock advanced conversational abilities, better context understanding, and more nuanced responses.

Remember to fill in the placeholders:

Replace <YOUR_REPOSITORY_URL_HERE> with your actual repository URL.
Specify the exact LLM or LLM service you integrated (e.g., “OpenAI GPT-4o”, “Claude 3 Opus”).
Mention if you’ve integrated FAISS or another Vector Database.
Add details about any other features you’ve implemented (e.g., Telegram Bot integration, Redis Queue, enhanced documentation).

