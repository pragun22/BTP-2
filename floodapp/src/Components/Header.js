import React, { useState } from 'react';
import './../styles/Header.css';
import { useHistory } from 'react-router-dom';

export default () => {

    const { push } = useHistory();

    return(
        <div className="header-container">
            <div className="nav-bar-container">
                <div 
                    className="nav-bar-element"
                    onClick={() => push('/')}
                >
                    <div className="nav-bar-text">
                        Home
                    </div>
                </div>
                <div 
                    className="nav-bar-element"
                    onClick={() => push('/data_input')}
                >
                    <div className="nav-bar-text">
                        Input Data
                    </div>
                </div>
            </div>
        </div>
    );
}