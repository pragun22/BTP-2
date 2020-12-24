This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
# Frontend Setup
* Install yarn. Follow the instructions given [here](https://classic.yarnpkg.com/en/docs/install/#debian-stable).
* Navigate to frontend directory using command line.
* Run ```yarn install```.
* Start the frontend server using ```yarn start```
# Deployment
Follow the following steps for deployment on Heroku.

* Create an account on Heroku
* Install Heroku CLI locally. Follow the steps mentioned [here](https://devcenter.heroku.com/articles/heroku-cli).
* Run ```heroku login``` command. You’ll be prompted to enter any key to go to your web browser to complete login. The CLI will then log you in automatically.
* Copy the contents of frontend app in a separate directory named frontend.
* Navigate to the new directory using ```cd frontend```.
* Run following commands
```
git init
heroku create -b https://github.com/mars/create-react-app-buildpack.git
git add .
git commit -m "deploy frontend"
git push heroku master
````
After deployment the app will be visible in Heroku dashboard and a public URL will be available for access.


# Routes
* **/** - Landing page. Contains form for city level flood inundation mapping.
* **/data_input** - Contains form for custom hydrology mapping.
* **rain_pred** -  Contains form where user can upload time series for rainfall prediction

# Files
* **Header.js** - Contains the navbar with links to all pages in the app.
* **Input.js** - Contains form for city level flood mapping. Also contains the function for overlaying generated plot on google map's interface.
* **dataInput.js** - Contains form for custom hydrology mapping. Also displays generated plot.
* **rainPrediction.js** - Contains form for rainfall prediction. Also displays generated plot.
