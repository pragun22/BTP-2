import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import TextField from '@material-ui/core/TextField';
import Input from '@material-ui/core/Input';
import './../styles/dataInput.css';

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
        <Container maxWidth="xs" className="container">
            <CssBaseline />
			<Typography component="h1" variant="h4" align="center">
				Input Data
			</Typography>
			<form onSubmit={this.handleUploadImage} className="form-div">
				<div className="input-div">
					<Typography component="h3" variant="h5" fon>
						DEM
					</Typography>
					<Input
						type="file"
						ref={(ref) => { this.uploadDem = ref; }}
						id="dem"
					/>
					
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						Infiltration
					</Typography>
					<Input
						type="file"
						ref={(ref) => { this.uploadInf = ref; }}
					/>
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						DEM
					</Typography>
					<Input
						type="file"
						ref={(ref) => { this.uploadSoil = ref; }}
					/>
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						Rainfall
					</Typography>
					<TextField
						variant="outlined"
						margin="normal"
						required
						fullWidth
						id="name"
						label="Enter the amount of rainfall in mm"
						name="Rain"
						autoComplete="name"
						ref={(ref) => { this.rainData = ref; }}
						autoFocus
					/>
				</div>
				<Button color="secondary">Upload</Button>
			</form>
		</Container>
    );
  }
}

export default UserInput;