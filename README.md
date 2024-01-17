# BhanGen_QuizWiz

# Test Maker Pro

Test Maker Pro is a web application built with Flask that allows users to generate tests using ChatGPT, sign up, log in, save tests, and retrieve saved tests.

## Features

- **Get Test**: Generate a test using ChatGPT with specified parameters.
- **Sign Up**: Create a new user account.
- **Login**: Log into an existing user account.
- **Save Test**: Save a generated test to the database.
- **Get Tests**: Retrieve a list of saved tests for a specific user.
- **Get Test Info**: Retrieve detailed information about a specific saved test.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/Test-Maker-Pro.git
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Set up MySQL database:

- Create a database named `test_maker_pro`.
- Update `mydb` configuration in `app.py` with your MySQL credentials.

4. Run the application:
  ```python
  python app.py
 ```

The application will be accessible at [http://localhost:5000/](http://localhost:5000/).

## API Endpoints

- **Get Test**: `/getTest` (POST)
- **Sign Up**: `/signup` (POST)
- **Login**: `/login` (POST)
- **Save Test**: `/saveTest` (POST)
- **Get Tests**: `/getTests` (POST)
- **Get Test Info**: `/getTestInfo` (POST)

## Usage

1. Use the provided API endpoints for the desired functionality.
2. Ensure proper JSON format for requests and responses.

## Dependencies

- Flask
- Flask-CORS
- OpenAI GPT-3
- MySQL Connector

### Table Schema 

- login Table
    - userId 
    - username
    - password 


- tests Table
    - testId
    - userId 
    - testName     
    -  gottenCorrect 

- questions Table
   - questionId
   -  testId
   -  question
   -  explanation 

- answerChoices 
  - answerChoiceId
  - questionId
  - answerChoice
  - correctAnswer 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

