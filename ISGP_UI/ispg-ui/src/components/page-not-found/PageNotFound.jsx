import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';

const PageNotFound = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '90vh',
        textAlign: 'center',
        //backgroundColor: '#f4f6f8',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundImage: 'url("/path-to-your-spectrum.gif")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.1,
          zIndex: -1,
        }}
      />

      {/* Content */}
      <Typography variant="h1" sx={{ fontSize: '3rem', mb: 2, color: '#1976d2' }}>
        Oops! Couldn't Find Page.
      </Typography>
      <Typography variant="body1" sx={{ fontSize: '1.25rem', mb: 4, color: '#1976d2' }}>
        It seems the page you're looking for is not resonating with our frequencies.
      </Typography>

      {/* Buttons */}
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          sx={{
            backgroundColor: '#1976d2',
            '&:hover': { backgroundColor: '#115293' },
          }}
          onClick={() => navigate('/')}
        >
          Return to Home
        </Button>
       
      </Box>
    </Box>
  );
};

export default PageNotFound;
