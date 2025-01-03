# Random Maze Generator Game

This project is a random maze generator game built using Streamlit. The application allows users to generate a random maze and attempt to solve it.

## Features

- Generate a random maze of customizable size.
- Visualize the maze in a user-friendly interface.
- Solve the maze and display the solution path.

## Project Structure

```
random-maze-generator
├── src
│   ├── app.py            # Entire Creation of the Maze in the Streamlit application
├── requirements.txt      # Lists the project dependencies
└── README.md             # Documentation for the project
```

## Requirements

To run this application, you need to install the following dependencies:

- streamlit
- numpy (if used for maze generation)
- any other libraries as needed

You can install the required packages using:

```
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application, navigate to the project directory and run:

```
streamlit run src/app.py
```

This will launch the application in your default web browser.