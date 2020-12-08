import React from 'react';
import {Route} from 'react-router-dom';
import App from './App';
import DataInput from './Components/dataInput';
import RainPrediction from './Components/rainPrediction';
import Header from './Components/Header';

const routes = [
	{
		"path":'/',
		"component":<App/>,
	},
	{
		"path":'/data_input',
		"component":<DataInput/>,
	},
    {
        "path":'/rain_pred',
        "component":<RainPrediction/>,
    },
];

const Routes = () => {
  
    return (
      <div>
        {routes.map(({path, component}) => (
            <Route
                exact
                key={path}
                path={path}
            >
                <Header/>
                <div className="component">
                    {component}
                </div>
            </Route>
        ))}
      </div>
    );
};

export default Routes;
