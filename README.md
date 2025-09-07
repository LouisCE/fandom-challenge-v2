# Fandom Challenge

Fandom Challenge is a Python terminal-based quiz game that runs in the Code Institute mock terminal on Heroku. Players can test their knowledge of different gaming franchises (Jak and Daxter, Ratchet & Clank, and God of War) through multiple-choice questions.

## User Goals

- Enjoy a fun and engaging terminal-based quiz experience.
- Test knowledge of multiple gaming franchises.
- Understand the quiz rules before playing.
- Play from any device that can run a Python terminal.
- Receive instant feedback on answers.
- Answer options are randomised each time to ensure true knowledge is tested.
- Replay quizzes for better results and enhanced replayability.

## User Stories

1. As a new player, I want to run the quiz easily from the terminal.
2. As a player, I want the quiz to randomise questions so each game feels fresh.
3. As a player, I want answer options to appear in different orders to prevent memorisation.
4. As a player, I want immediate feedback after answering so I know if I was correct or incorrect.
5. As a player, I want to see my final score and high scores at the end.
6. As a player, I want different outcomes depending on my performance.
7. As a returning player, I want my high scores to persist between sessions for long-term progress.
8. As a player, I want to be able to replay the quiz without restarting the program.

## Features

- Choose from multiple quiz categories (Jak and Daxter, Ratchet & Clank, God of War).
- Randomised questions within each quiz.
- Color-coded feedback for correct and incorrect answers.
- Score tracking and end-of-quiz results.
- Replay option to try again.

## Technologies Used

- **Python 3:** Core programming language.
- **Colorama:** For colored terminal output.
- **Heroku:** Deployment platform.
- **GitHub:** Version control and source code hosting.

## Testing

Testing included:

- Manual testing of input handling and score calculation.
- Verifying randomisation of questions and answer order.
- Deployment testing on Heroku terminal.
- Error handling for invalid input or empty answers.

## Deployment

This project was deployed using Heroku:

1. Fork or clone this repository.
2. Create a new Heroku app.
3. In the **Settings** tab, add the following buildpacks in order:
   - `heroku/python`
   - `heroku/nodejs`
4. Set a config var:
   - `PORT` = `8000`
5. Connect the Heroku app to your GitHub repository.
6. Deploy the main branch manually, or enable automatic deploys.

The live deployed app can be found here:  
[Fandom Challenge V2 on Heroku](https://fandom-challenge-v2-a2c443c8af3e.herokuapp.com/)

## Credits

- Developed by LouisCE for Code Institute Portfolio Project 3.
- Thanks to Code Institute for the deployment template.