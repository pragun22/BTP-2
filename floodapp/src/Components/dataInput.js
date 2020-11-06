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
      responseData: '',
      responseReceived: false,
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();
    const data = new FormData();
    data.append('dem', this.uploadDem);
    data.append('rain', this.rainData);
    data.append('infil', this.uploadInf);
    data.append('soil', this.uploadSoil);
    data.append('rain', this.uploadRain);
		fetch('http://localhost:8081/custom_data', {
			method: 'POST',
			body: data,
		}).then((response) => {
			response.json().then((body) => {
				this.setState({
					responseData: body.url
				})
				this.setState({
					responseReceived: true
				})
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
			<>{!this.state.responseReceived && <form onSubmit={this.handleUploadImage} className="form-div">
				<div className="input-div">
					<Typography component="h3" variant="h5">
						DEM
					</Typography>
					<Input
						type="file"
						 onInput={ e=>{this.uploadDem = e.target.files[0]}}
						// ref={(ref) => { this.uploadDem = ref; }}
						id="dem"
					/>
					
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						Infiltration
					</Typography>
					<Input
						type="file"
						 onInput={ e=>{this.uploadInf = e.target.files[0]}}
						// ref={(ref) => { this.uploadInf = ref; }}
					/>
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						Soil
					</Typography>
					<Input
						type="file"
						 onInput={ e=>{this.uploadSoil = e.target.files[0]}}
						// ref={(ref) => { this.uploadSoil = ref; }}
					/>
				</div>
				<div className="input-div">
					<Typography component="h3" variant="h5">
						Rainfall
					</Typography>
					<TextField
						variant="outlined"
						margin="normal"
						fullWidth
						id="name"
						label="Enter the amount of rainfall in mm"
						name="Rain"
						autoComplete="name"
						 onInput={ e=>{this.rainData = e.target.value}}

						// ref={(ref) => { this.rainData = ref; }}
						autoFocus
					/>
				</div>
				<Typography component="h3" variant="h5">
						<center>OR</center>
				</Typography>
				<div className="input-div">
					<Input
						type="file"
						 onInput={ e=>{this.uploadRain = e.target.files[0]}}
						// ref={(ref) => { this.uploadSoil = ref; }}
					/>
				</div>
				<Button type = "submit" color="secondary">Upload</Button>
			</form>}</>
			<>{this.state.responseReceived &&<div> <img src={this.state.responseData} width="400" height="400" /></div>}</>
		</Container>

    );
  }
}

export default UserInput;