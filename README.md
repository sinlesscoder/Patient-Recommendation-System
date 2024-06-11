## Clinician Patient Support Web Application

This project is a web application and patient insight utility for doctors built with Flask, providing functionalities for text and image processing. Users can upload text files and images, and the application offers three main features for AI-enabled patient understanding for clinicians:

1. **Text Summarization**: Summarize text files using OpenAI's GPT-4 model with a structure that captures the patient's problem, current complications, and recommendations to make it faster for a clinician to audit and get the patient necessary support.
2. **Entity Extraction**: Extract relevant information from a clinical perspective from text files and present the information in a tabular format.
3. **Question Answering**: Utilize Weaviate's vector database to answer questions based on the content of uploaded text files via retrieval augmented generation (RAG).

### Functionality Overview

#### 1. Text Summarization

- **Interaction**: Users upload a text file, and the application leverages OpenAI's GPT-4 model to generate a summary of the text content.
- **Implementation**: The Flask route `/process/<filename>` handles the text summarization functionality. It utilizes the `summary_chain` method from the `Tasks` class, which interacts with the OpenAI model to produce the summary.

#### 2. Entity Extraction

- **Interaction**: Users upload a text file, and the application extracts key information from the text, such as dates, chief complaints, medications, procedures, and smoking history, presenting it in a tabular format.
- **Implementation**: The Flask route `/process/<filename>` also handles entity extraction. It utilizes the `extract_entities` method from the `Tasks` class, which interacts with the text to extract relevant entities.

#### 3. Question Answering with RAG

- **Interaction**: Users can ask questions related to the content of the uploaded text file, and the application retrieves answers using Weaviate's vector database.
- **Implementation**: The Flask route `/qa/<filename>` handles the question-answering functionality. It utilizes the `question_answer` method from the `Tasks` class, which interacts with the Weaviate vector database to find relevant answers.

### Application Flow

1. **Upload Files**: Users upload text files and images through the web interface.
2. **Choose Functionality**: After uploading a text file, users can select one of the three functionalities: summarize text, extract entities, or ask questions.
3. **Processing**: The selected functionality is executed based on the uploaded text file.
4. **Display Results**: The application displays the results of the chosen operation to the user.

### Development and Contribution

- **Setting Up for Development**: Fork the repository, clone it to your local machine, and create a new branch for your feature or bug fix.
- **Development Workflow**: Make changes to the codebase, test thoroughly, and submit pull requests with clear descriptions.
- **Reporting Issues**: If you encounter any issues or have suggestions for improvements, please report them in the GitHub issues section.

### Requirements

- Python 3.10+
- Flask
- OpenAI API key
- Docker

### Setup Instructions

1. Create a virtual environment and install the modules found in `weaviate/flask_app/requirements.txt` via pip.

```bash
pip install requirements.txt
```

2. Assuming Docker Desktop is enabled, navigate to the directory containing the `docker-compose.yml` file found at `weaviate/vector_db` and startup the Weaviate vector database using `docker-compose up`.

```bash
docker-compose up -d
```

3. Start the Flask application.

```bash
python weaviate/flask_app/app.py
```



