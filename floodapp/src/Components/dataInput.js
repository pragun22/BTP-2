import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import axios from 'axios'
export default () => {
    const [dem,setDem] = useState();
    const [infil,setInfil] = useState();
    const [soil,setSoil] = useState();
    const [rain,setRain] = useState();
    const [isSubmit,setIsSubmit] = useState(0);
    async function handleSubmit(){
        // console.log("dem = ",dem);
        // console.log("infil = ",infil);
        // console.log("soil = ",soil);
        // console.log("rain = ",rain);

        let data = new FormData();
        data.append('dem',dem);
        data.append('infil',infil);
        data.append('soil',soil);
        data.append('rain',rain);
        axios.post('http://localhost:5000/custom_data',data)
        .then(response => setIsSubmit(1))
        .catch(error => {
            setIsSubmit(2);
        })

    }

    function upload(e,type){
        if(type === 'dem'){
            // console.log("dem = ",e.target.files[0]);
            setDem(e.target.files[0]);
        }
        if(type === 'infil'){
            // console.log("inf = ",e.target.files[0]);
            setInfil(e.target.files[0]);
        }
        if(type === 'soil'){
            // console.log("soil = ",e.target.files[0]);
            setSoil(e.target.files[0]);
        }
        if(type === 'rain'){
            // console.log("rain = ",e.target.value);
            setRain(e.target.value);
        }
    }

    return(
        <Container maxWidth="sm">
            <CssBaseline />
            <div>
                <Typography component="h1" variant="h5">
                Enter Details
                </Typography>
                {/* <form noValidate> */}
                <input
                    type="file"
                    name="dem_data"
                    onChange={(e) => upload(e,'dem')}
                    required
                />
                <input
                    type="file"
                    name="inf_data"
                    onChange={(e) => upload(e,'infil')}
                    // required
                />
                <input
                    type="file"
                    name="soil_data"
                    onChange={(e) => upload(e,'soil')}
                    // required
                />
                <input
                    type="text"
                    name="rain_data"
                    onBlur={(e) => upload(e,'rain')}
                    required
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick = {() => handleSubmit()}
                >
                    Search
                </Button>
                {/* </form> */}
            </div>
            <div>
            {
                isSubmit == 1 ?
                (
                    <div>
                        Files uploaded
                    </div>
                ):
                (<></>)
            }
            {
                isSubmit == 2 ?
                (
                    <div>
                        Error in File uploading
                    </div>
                ):
                (<></>)
            }
            </div>
            <Box mt={8}>
                {/* <Copyright />    */}
            </Box>
        </Container>
    )
        
}