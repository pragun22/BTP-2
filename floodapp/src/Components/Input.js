import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import AppBar from '@material-ui/core/AppBar';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

class Input extends React.Component {
    constructor(props){
        super(props);
        var today = new Date();
        this.state={
            date: today.getFullYear() + '-' + (today.getMonth() <= '9' ? '0'+today.getMonth(): today.getMonth()) + '-' + today.getDate(),
        }
    }
    render(){
        var today = new Date();
        console.log(today);
        console.log(this.state.date)
        const {classes} = this.props;
        return(
        <Container component="main" maxWidth="xs" className={classes.container}>
            <CssBaseline />
            <div className={classes.paper}>
                <Typography component="h1" variant="h5" className={classes.text}>
                Enter Details
                </Typography>
                <form className={classes.form} noValidate>
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
                </form>
            </div>
            <Box mt={8}>
                {/* <Copyright />    */}
            </Box>
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