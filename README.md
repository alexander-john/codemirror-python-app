# CodeMirror Python Practice with Error Feedback

This project is a web-based Python code practice tool that provides real-time error feedback using CodeMirror. Users can write Python functions and get immediate feedback on their code.

## Features

- CodeMirror editor with Python syntax highlighting
- Real-time linting and error feedback
- Customizable themes and linting options
- Feedback display for success and error messages

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- CodeMirror

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/codemirror-python-practice.git
    cd codemirror-python-practice
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    # On Windows use 
    `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the App

1. Start the Flask server:
    ```sh
    python server.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

## Usage

- Write your Python functions in the CodeMirror editor.
- Click the "Validate" button to check your code.
- Feedback will be displayed below the editor.
