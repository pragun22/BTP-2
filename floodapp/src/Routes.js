import React from 'react';
import {Route} from 'react-router-dom';
import App from './App';
import DataInput from './Components/dataInput';

const routes = [
	{
		"path":'/',
		"component":<App/>,
	},
	{
		"path":'/data_input',
		"component":<DataInput/>,
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
                <div className="component">
                    {component}
                </div>
            </Route>
        ))}
      </div>
    );
};

export default Routes;
