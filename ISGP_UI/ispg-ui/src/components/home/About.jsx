import React from 'react'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import DNAGifImage from '../../images/DNAGif2.gif';

const commonStyles = {
    display:'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap:'25px',
    padding:'15px',
    //fontWeight: 'bold',
    margin:'0',
    height: '90vh',

  };

  const image = {
    width: '20%', /* Adjust width as needed */
    height: '75px' /* Maintain aspect ratio */
  }
const About = () => {
  return (
    <Box >
       
       
    <Box sx={commonStyles}>
        
         <Typography variant="body1" component="p">
         <Typography variant="h2" component="p"> What is ISGP? <br></br></Typography>
       Impedance Spectroscopy by Genetic Programming (ISGP) has been developed to solve the ill-posed inverse 
       problem of seeking a distribution function of relaxation times (DFT) from IS experimental results. <br></br>
       The prior knowledge used is to assume the Debye kernel for dielectric systems and to assume that the DFT is a 
       combination of simple peaks. An evolutionary programming technique, GP, is used to identify "the best" DFT. <br></br>
       Assessment of each model is done taking into account its complexity and the fitness of its prediction to the measured data.
      </Typography>
      <img src={DNAGifImage} alt="Image" sx={image} />
      {/* <Card sx={{ minWidth: 250 }}>
         <CardMedia
        sx={{ height: 275 }}
        image={DNAImage}
        title="DNA"
      />
        </Card> */}
        </Box>
      </Box>
  )
}

export default About
