# My FastAPI Project
## Run
pip install -r requirements.txt
uvicorn app.main:app --reload

.env example file:
```
GOOGLE_API_KEY = "your_google_api_key"

QDRANT_URL = "https://3fcb8886-b81b-4551-b2d9-1ed17d630ce2.eu-west-2-0.aws.cloud.qdrant.io"

QDRANT_API_KEY = "your_qdrant_api_key"