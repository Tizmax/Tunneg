# Flask Application README

# Flask Tunneg Game

This project is a Flask web application that replicates the functionality of the original Streamlit application found in `tunneg.py`. It provides an interactive game experience where players can select themes and track their progress.

## Project Structure

```
flask-app
├── app
│   ├── __init__.py          # Initializes the Flask application and configuration
│   ├── routes.py            # Defines the application routes and game logic
│   └── templates
│       └── index.html       # Main HTML template for the application
├── static
│   └── style.css            # CSS styles for the application
├── tunneg.py                # Original Streamlit code for reference
├── requirements.txt         # Lists the dependencies for the application
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   flask run
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Players can select from various themes and engage in the game.
- The application tracks player progress and displays it dynamically.
- The game state is managed through session variables.

## Dependencies

- Flask
- Any other libraries specified in `requirements.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.