import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import { withStyles } from '@material-ui/core/styles';

class UserInput extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('dem', this.uploadDem.files[0]);
    data.append('rain', this.rainData.value);
    data.append('infil', this.uploadInf.files[0]);
    data.append('soil', this.uploadSoil.files[0]);
    fetch('http://localhost:8081/custom_data', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
      	console.log(response);
      });
    });
  }

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
        DEM
          <input ref={(ref) => { this.uploadDem = ref; }} type="file" />
        </div>
        <br />
        <div>
        <div>
        Infiltration
          <input ref={(ref) => { this.uploadInf = ref; }} type="file" />
        </div>
        <br />
        <div>
        Soil
          <input ref={(ref) => { this.uploadSoil = ref; }} type="file" />
        </div>
        <br />
        <div>
          <input ref={(ref) => { this.rainData = ref; }} type="text" placeholder="Enter the amount of rainfall in mm" />
        </div>
        <br />
          <button>Upload</button>
        </div>
      </form>
    );
  }
}

export default UserInput;