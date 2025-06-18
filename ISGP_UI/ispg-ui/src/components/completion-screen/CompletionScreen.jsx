import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button, useTheme } from '@mui/material';

const CompletionScreen = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '70vh',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden',
       // bgcolor: theme.palette.background.default, // Use theme background color
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
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.1,
          zIndex: -1,
        }}
      />

      {/* Content */}
      <Typography variant="h1" sx={{ mb: 2, color: theme.palette.primary.main }}>
        Evolution Completed
      </Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        The algorithm has finished running successfully.
      </Typography>

      {/* Buttons */}
      <Box sx={{ display: 'flex', gap: theme.spacing(2) }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/')}
        >
          Return to Home
        </Button>
      </Box>
    </Box>
  );
};

export default CompletionScreen;
