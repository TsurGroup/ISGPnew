import React from 'react';
import Box from '@mui/material/Box';
import Fade from '@mui/material/Fade';

const commonStyles = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: '35px',
  margin: '0',
  height: '90vh',
};

const WelcomeMessage = () => {
  return (
    <Box sx={commonStyles}>
      <Fade appear={true} in={true} timeout={8000}>
        <Box textAlign="center">
          <div>Welcome To</div>
          <div>Impedance Spectroscopy Genetic Programming</div>
        </Box>
      </Fade>
    </Box>
  );
};

export default WelcomeMessage;