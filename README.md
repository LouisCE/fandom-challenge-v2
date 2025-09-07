# Fandom Challenge

Fandom Challenge is a Python terminal-based quiz game that runs in the Code Institute mock terminal on Heroku. Players can test their knowledge of different gaming franchises (Jak and Daxter, Ratchet & Clank, and God of War) through multiple-choice questions.

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