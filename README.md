# PostSync API 🚀

PostSync is the core backend engine for an AI social media automation agency. 
It uses OpenAI (GPT-4o) to intelligently rewrite single content pieces into platform-optimized posts (Twitter thread summaries vs. LinkedIn professional posts vs. Instagram engaging captions). It then uses the Ayrshare API to automatically publish these posts simultaneously.

## Tech Stack
- **Framework**: FastAPI (Python)
- **AI Brain**: OpenAI API
- **Publishing Engine**: Ayrshare

## Project Structure
- `main.py`: The core FastAPI application and API routes.
- `services/ai_service.py`: Handles connection to OpenAI and dynamic prompt generation tailored per platform.
- `services/ayrshare_service.py`: Handles publishing posts and images to multiple platforms through the Ayrshare integration.

## Getting Started

### 1. Prerequisites
- Python 3.9+
- API keys for OpenAI and Ayrshare

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd PostSync

# Set up the virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY="your_openai_api_key_here"
AYRSHARE_API_KEY="your_ayrshare_api_key_here"
```

### 4. Running the Server
```bash
uvicorn main:app --reload
```
Once the server is running, you can test the API by navigating to the interactive Swagger UI at:
**http://127.0.0.1:8000/docs**
