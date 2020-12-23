This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
# Frontend Setup
* Install yarn. Follow the instructions given [here](https://classic.yarnpkg.com/en/docs/install/#debian-stable).
* Navigate to frontend directory using command line.
* Run ```yarn install```.
* Start the frontend server using ```yarn start```

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

# Routes
* **/** - Landing page. Contains form for city level flood inundation mapping.
* **/data_input** - Contains form for custom hydrology mapping.
* **rain_pred** -  Contains form where user can upload time series for rainfall prediction

# Files
* **Header.js** - Contains the navbar with links to all pages in the app.
* **Input.js** - Contains form for city level flood mapping. Also contains the function for overlaying generated plot on google map's interface.
* **dataInput.js** - Contains form for custom hydrology mapping. Also displays generated plot.
* **rainPrediction.js** - Contains form for rainfall prediction. Also displays generated plot.
