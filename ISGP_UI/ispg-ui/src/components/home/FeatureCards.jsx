import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

import backgroundImage from '../../images/github1.png';

const containerStyles = {
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'space-between',
  height: '90vh',
  padding: '0 40px', // Adds space on the sides of the container
  gap: '75px'
};

const textContainerStyles = {
  maxWidth: '80%', // Limits text width to keep it on the left
};

const imageContainerStyles = {
  display: 'flex',
  justifyContent: 'flex-end', // Aligns image to the right
  flexGrow: 1, // Pushes the image to the right edge of the container
};

const imageStyles = {
  width: '500px', // Adjust width as needed
  height: 'auto', // Maintains aspect ratio
  marginLeft: '20px', // Adds a gap between the text and the image
};

const handleClick = () => {
  // Replace the URL with your GitHub repository link
  window.open('https://github.com/shem221/ISGP', '_blank');
};

const FeatureCards = () => {
  return (
    <Box sx={containerStyles}>
      {/* Left side - Text */}
      <Box sx={textContainerStyles}>
        <Typography variant="h2" component="p" gutterBottom>
          Open Source
        </Typography>
        <Typography variant="body1" component="p">
          Check out our GitHub repository for more details!
        </Typography>
        <Button
          onClick={handleClick}
          style={{ padding: '10px 20px', fontSize: '16px', marginTop: '20px' }}
          variant="contained"
          color="primary"
        >
          Open GitHub Repository
        </Button>
      </Box>

      {/* Right side - Image */}
      <Box sx={imageContainerStyles}>
        <img src={backgroundImage} alt="GitHub Logo" style={imageStyles} />
      </Box>
    </Box>
  );
};

export default FeatureCards;
