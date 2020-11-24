import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { 
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  GroundOverlay } from "react-google-maps"
class Input extends React.Component {
    constructor(props){
        super(props);
        var today = new Date();
        this.state={
        	date: today.getFullYear() + '-' + (today.getMonth() <= '9' ? '0'+today.getMonth(): today.getMonth()) + '-' + today.getDate(),
      		responseReceived: false,
      		url:'',
      		center:'',
      		bbox:'',
      		MapWithGroundOverlay:''
        }
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.handleMap = this.handleMap.bind(this);
    }
    handleMap(){
   	const { compose } = require("recompose");
	const {
	  withScriptjs,
	  withGoogleMap,
	  GoogleMap,
	  GroundOverlay,
	} = require("react-google-maps");
	    this.state.MapWithGroundOverlay = compose(
	  withScriptjs,
	  withGoogleMap
	)(props =>
	  <GoogleMap
	    defaultZoom={12}
	    defaultCenter={{lat: this.state.center[1], lng: this.state.center[0]}}
	  >
	    <GroundOverlay
	      defaultUrl={this.state.url}
	      defaultBounds={new window.google.maps.LatLngBounds(
	        new window.google.maps.LatLng(this.state.bbox[1], this.state.bbox[0]),
	        new window.google.maps.LatLng(this.state.bbox[3], this.state.bbox[2])
	      )}
	      defaultOpacity={0.3}
	    />
	  </GoogleMap>
);
    }
    handleSubmit(ev) {
    ev.preventDefault();
    const data = new FormData();
    data.append('city', this.uploadCity);
    data.append('date', this.uploadDate);
		fetch('http://localhost:8081/get_map', {
			method: 'POST',
			body: data,
		}).then((response) => {
			response.json().then((body) => {
				this.setState({
					url:body.url
				})
				this.setState({
					center: body.centre
				})
				this.setState({
					bbox: body.bbox
				})
				
				this.handleMap();
				this.setState({
					responseReceived: true
				})

			});
		});
  }
    render(){
        var today = new Date();
        const {classes} = this.props;
        return(
        <Container component="main" maxWidth="xs" className={classes.container}>
            <CssBaseline />
            <div className={classes.paper}>
                <Typography component="h1" variant="h5" className={classes.text}>
                Enter Details
                </Typography>
                <>{!this.state.responseReceived && <form className={classes.form} onSubmit={this.handleSubmit}  noValidate>
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    id="name"
                    label="City Name"
                    name="name"
                    autoComplete="name"
                    autoFocus
					onInput={ e=>{this.uploadCity = e.target.value}}
                />
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    id="date"
                    label="Enter Date"
                    type="date"
                    defaultValue={this.state.date}
					onInput={ e=>{this.uploadDate = e.target.value}}
                    autoComplete="Date"
                    autoFocus
                    InputLabelProps={{
                    shrink: true,
                    }}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    className={classes.submit}
                >
                    Search
                </Button>
                </form>}</>
			<>{this.state.responseReceived &&<Container component="main" maxWidth="xs" className={classes.container}>
			<this.state.MapWithGroundOverlay
		        googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyDUjKlnObDJwUO6f2ueMvzc3UyF_Jepd5U&v=3.exp&libraries=geometry,drawing,places"
		        loadingElement={<div style={{ height: `100%` }} />}
		        containerElement={<div style={{ height: `400px` }} />}
		        mapElement={<div style={{ height: `100%` }} />}
		      />
			</Container> }</>
            </div>
           
        </Container>
        );
    }
}

const Styles = theme => ({
    paper: {
      marginTop: theme.spacing(8),
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
    container:{
      backgroundColor: '#FFFFFF',
      borderRadius: '10%',
      paddingTop: '3%',
      paddingBottom: '3%',
    },
    text:{
        color: '#282c34',
    },
    avatar: {
      margin: theme.spacing(1),
      backgroundColor: theme.palette.secondary.main,
    },
    form: {
      width: '100%', // Fix IE 11 issue.
      marginTop: theme.spacing(1),
    },
    submit: {
      margin: theme.spacing(3, 0, 2),
    },
    title: {
        flexGrow: 1,
      },
  });

  export default withStyles(Styles)(Input);