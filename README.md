# Neuramonks_Assignment

This repository contains a Streamlit application for a question-answering system integrated with various data sources such as PDF and CSV files. The application allows users to upload their files, ask questions, and receive answers based on the content of the uploaded documents.
#### Live Demo : https://4170-2409-40c1-4a-33a0-e840-d553-61f7-93de.ngrok-free.app/

### Features:

- **Upload Files**: Users can upload PDF and CSV files containing the data they want to query.
- **Question-Answering**: Users can ask questions related to the content of the uploaded files.
- **Multi-Source Integration**: The system supports both PDF and CSV formats for data retrieval and question-answering.
- **Responsive Interface**: The Streamlit interface dynamically updates as users interact with the application, providing a seamless experience.

### Installation:

1. Clone the repository:
```commandline
git clone https://github.com/VandanC/Neuramonks_Assignment.git
```

2. Install the required dependencies:
```commandline
pip install -r requirements.txt
```

3. Configure '.env' file:
```commandline
GOOGLE_API_KEY=your_google_api_key_here
```

### Usage:

1. Navigate to the directory containing the cloned repository.

2. Run the Streamlit application:

```commandline
streamlit run main.py
```

3. Access the application through the provided local host link in your web browser.

4. Upload PDF and CSV files containing the data you want to query.

5. Ask questions related to the content of the uploaded files using the chat interface.

### Notes:

- Ensure that you have the necessary  credentials for accessing the Google Gemini API services used in the application.
- Currently, only ';' separated CSVs are supported


## Hosting the Application using ngrok

ngrok is a tool that allows you to expose your local development server to the internet. 
Below are instructions for installing ngrok on windows operating systems and how to use it to host your local port.
Follow the steps after 

- Step 1: Download zip from [ngrok website](https://ngrok.com/download).
- Step 2: Add authtoken
    ```commandline
    ngrok config add-authtoken <token>
    ```
- Step 3: Open the terminal in the file path where the zip file was extracted, and start the tunnel
    ```commandline
    .\ngrok.exe http <port>
    ```
  * Streamlit usually uses 8501 port number

_To install and use ngrok on other operating systems please refer [ngrok website](https://ngrok.com/download)._

