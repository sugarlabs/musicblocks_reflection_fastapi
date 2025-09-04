# AI Tool for Reflection - Developer Guide

## Overview

Welcome to the developer's guide of the FastAPI backend for the Reflection widget.

## Contents :

[1. Client–Server Architecture Diagram](#client–server-architecture-diagram)  
[2. Local Setup Guide for FastAPI Music Blocks Backend](#local-setup-guide-for-fastapi-musicblocks-backend)  
[3. API Endpoints](#api-endpoints)  
[4. Retriever Module `retriever.py`](#retriever-module-retrieverpy)  
[5. Related Files](#related-files)  
[6. AWS Deployment Guide](#aws-deployment-guide)

---

## Client–Server Architecture Diagram

![Architecture Diagram](./docs/images/architecture.svg)

## Local Setup Guide for FastAPI MusicBlocks Backend

### Prerequisites

- **Python 3.10+** installed
- **Google API Key** for Gemini models
- **Qdrant** running locally or via cloud for RAG

### Steps

#### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Commanderk3/musicblocks_reflection_fastapi.git
```

```bash
cd musicblocks_reflection_fastapi
```

#### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

```bash
.\.venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a .env file in the project root with your keys:

```env
GOOGLE_API_KEY=google_api_key
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=qdrant_api_key
```

Or edit config.py directly with your values.

#### 5. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

---

## API Endpoints

### 1. `/projectcode/`

**POST**  
Analyzes user project code and returns a structured algorithm summary.

- **Request Body:**

  - `code` (str): JSON string of the user’s project code.

- **Response:**

  - `algorithm` (str): Parsed algorithm summary.
  - `response` (str): LLM-generated explanation.

- **Function:**
  - The backend receives a code parameter containing the Music Blocks project code as a string.
  - This code is passed to `convert_music_blocks(code)`, which transforms it into a flowchart representation that is easier for the LLM to interpret.
  - To provide additional context, `findBlockInfo(flowchart)` is used to retrieve details about the individual blocks.
  - The resulting data is then passed into the `generateAlgorithmPrompt(flowchart, blockInfo)` template, which is used to invoke the LLM.

### 2. `/chat/`

**POST**  
Handles chat interactions with mentors, using context and structured prompts.

- **Request Body:**

  - `query` (str): User’s message.
  - `messages` (List[Dict]): Conversation history.
  - `mentor` (str): Mentor type (`meta`, `music`, `code`).
  - `algorithm` (str): Algorithm summary.

- **Response:**

  - `response` (str): LLM-generated reply.

- **Function:**
  - The incoming message is first converted into a LangChain message object. This format is better understood by the LLM and helps prevent ambiguity.
  - The system prompt is then updated using the mentor configuration, based on the provided mentor string.
  - Next, `getContext(query)` is used to retrieve the three most relevant context entries, which are injected into the message sequence.
  - Finally, the user query is appended as a HumanMessage, and the LLM is invoked with the complete LangChain message object.

### 3. `/analysis/`

**POST**  
Generates a summary analysis of the conversation.

- **Request Body:**

  - `messages` (List[Dict]): Conversation history.
  - `summary` (str): Previous summary.

- **Response:**

  - `response` (str): LLM-generated analysis.

- **Function:**
  - The incoming request contains two objects: messages and old analysis report.
  - These are passed to `generateAnalysis(old_summary, raw_messages)`, which produces a prompt for generating the analysis. The prompt is then executed by the LLM.

### 4. `/updatecode/`

**POST**  
Generates a new algorithm for the updated code and provides a response asking the user to confirm whether its understanding of the changes is correct.

- **Request Body:**

  - `oldcode` (str): JSON string of the previous project code.
  - `newcode` (str): JSON string of the new project code.

- **Response:**

  - `response` (str): LLM-generated analysis.
  - `algorithm` (str): New algorithmic summary.

- **Function:**
  -  Both codes will be converted into flowchart representations. If the flowcharts match, the LLM won’t be called.


## Retriever Module `retriever.py`

**Tools used**:

- Embedding Model: `sentence-transformers/all-MiniLM-L6-v2`
- LLM: `gemini-2.0-flash`, `gemini-2.5-flash`
- Vector Database: Qdrant Cluster

**Configuration**:

- LLM Temperature: `0.7`
- Relevance Threshold: `0.3` (distance metric, so lower is more relevant)
- Top-k chunks: `3`

This module provides retrieval-augmented generation (RAG) capabilities for the FastAPI backend. It initializes a Qdrant vector store using HuggingFace embeddings and connects to a Qdrant instance. It uses similarity search method against the "mb_docs" collection and returns relevant document context for a given query, which is used to enhance LLM responses.

For the `/projectcode` and `/analysis` endpoints, gemini-2.5-flash is used, as its built-in reasoning capability is enabled by default. For the `/chat` endpoint, gemini-2.0-flash is used instead. Since the current LangChain methods do not provide a way to control the reasoning feature of the Gemini-2.5 series, this custom arrangement was chosen.

## Related Files

- utils/prompts.py: Prompt templates and generation functions.
- utils/parser.py: MusicBlocks code parsing.
- utils/blocks.py: Block info extraction.
- retriever.py: RAG context retrieval.
- config.py: Configuration.

---

## AWS Deployment Guide

- **EC2 Instance Configuration**:

  - Instance Type: t3.micro (2 vCPUs, 1 GiB RAM)
  - OS: Ubuntu 22.04 LTS
  - Security Groups: Allow inbound on ports 22 (SSH), 80 (HTTP), 443 (HTTPS), and 8000 (Custom TCP for FastAPI)

- **Setup Steps**:

  1. SSH into the EC2 instance:
     ```bash
     ssh -i "reflection.pem" ubuntu@52.65.37.66
     ```
  2. Update and install dependencies:

     ```bash
     sudo apt update && sudo apt upgrade -y
     sudo apt install python3 python3-pip python3-venv -y
     ```

  3. Disk space was limited on t3.micro instances. `/dev/nvme0n1p1` initially had 14 GB even though the storage instance was set to 25 GB. To fix this, the partition was resized:

     ```bash
     sudo growpart /dev/nvme0n1 1
     ```

     Resize the filesystem:

     ```bash
     sudo resize2fs /dev/nvme0n1p1
     ```

     Verify the new size:

     ```bash
     df -h
     ```

  4. Memory was also limited (1 GB RAM), and hence the server would crash on startup. To fix this, a swap file was created:

     ```bash
     sudo fallocate -l 2G /swapfile
     sudo chmod 600 /swapfile
     sudo mkswap /swapfile
     sudo swapon /swapfile
     ```

  - Make the swap file permanent:

    ```bash
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    ```

  - Verify the swap is active:

    ```bash
    free -h
    ```

  4. Clone the repository:

     ```bash
     git clone https://github.com/Commanderk3/musicblocks_reflection_fastapi.git
     ```

     ```bash
     cd musicblocks_reflection_fastapi
     ```

  5. Create and activate a virtual environment:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
  6. Install dependencies:

     ```bash
      pip install -r requirements.txt
     ```

     **Note**: Make sure the `requirements.txt` file is compatible with linux.

  7. Configure environment variables:

     ```bash
     nano .env
     ```

     Add your keys:

     ```env
     GOOGLE_API_KEY=google_api_key
     EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
     QDRANT_URL=qdrant_cloud_url
     QDRANT_API_KEY=qdrant_api_key
     ```

     Save and exit (Ctrl+X, Y, Enter).

  8. Check the FastAPI server:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8000
     ```

  9. To run the server in the background, create a systemd service:

     ```bash
     sudo nano /etc/systemd/system/fastapi.service
     ```

     Add this configuration:

     ```ini

        [Unit]
        Description=FastAPI MusicBlocks Application
        After=network.target

        [Service]
        User=ubuntu
        Group=ubuntu
        WorkingDirectory=/home/ubuntu/musicblocks_reflection_fastapi
        Environment=PYTHONPATH=/home/ubuntu/musicblocks_reflection_fastapi
        EnvironmentFile=/home/ubuntu/musicblocks_reflection_fastapi/.env

        # Command to execute
        ExecStart=/home/ubuntu/musicblocks_reflection_fastapi/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

        # Restart on failure
        Restart=always
        RestartSec=5

        # Security
        NoNewPrivileges=yes
        PrivateTmp=yes

        [Install]
        WantedBy=multi-user.target
     ```

     Save and exit (Ctrl+X, Y, Enter).

  10. Reload systemd to recognize the new service:

      ```bash
      # Reload systemd to recognize new service
      sudo systemctl daemon-reload
 
      # Enable to start on boot
      sudo systemctl enable fastapi.service
 
      # Start the service now
      sudo systemctl start fastapi.service
 
      # Check status
      sudo systemctl status fastapi.service
      ```

## How to update the server with new code changes

1. SSH into the EC2 instance:
   ```bash
   ssh -i "reflection.pem" ubuntu@52.65.37.66
   ```
2. Navigate to the project directory:
   ```bash
   cd musicblocks_reflection_fastapi
   ```
3. Pull the latest changes from GitHub:

   ```bash
   git pull origin main
   ```

   Upstream repository: `https://github.com/Commanderk3/musicblocks_reflection_fastapi.git`

4. If there are new dependencies, install them:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   deactivate
   ```
5. Restart the systemd service to apply changes:
   ```bash
   sudo systemctl restart fastapi
   ```
6. Check the status to ensure it's running:
   ```bash
   sudo systemctl status fastapi
   ```
## License
Music Blocks Reflection FastAPI is licensed under the [GNU AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html). 
It does not collect, store, or share any kind of user data. 

Contributions are welcome. Please open issues or pull requests.