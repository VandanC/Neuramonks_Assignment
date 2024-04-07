# Neuramonks_Assignment

This repository contains a Streamlit application for a question-answering system integrated with various data sources such as PDF and CSV files. The application allows users to upload their files, ask questions, and receive answers based on the content of the uploaded documents.

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

