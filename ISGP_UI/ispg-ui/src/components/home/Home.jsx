import * as React from 'react';
import Box from '@mui/material/Box';
import WelcomeMessage from './WelcomeMessage';
import FeatureCards from './FeatureCards';
import About from './About';
import TOS from './TOS';
import VersionDialog from './VersionDialog';

import HomeService from '../../services/HomeService.js'

import { Fade } from "react-awesome-reveal";
import { useNavigate } from 'react-router-dom'; 
import { useState } from 'react';

const commonStyles = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: '16px', // Add spacing between sections
  backgroundSize: 'cover',
  backgroundRepeat: 'no-repeat',
  minHeight: '100vh', // Allow content to grow beyond the viewport
  padding: '10px',
  boxSizing: 'border-box', // Ensure padding is included in height calculations
};

const Home = ({ setVersion }) => {
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const sessionData = await HomeService.login();
      console.log('Login successful! Session data:', sessionData);
      navigate('/Data');
    } catch (error) {
      setError('Error logging in. Please try again.');
      console.error('Login error:', error);
    }
  };

  return (
    <Box style={commonStyles}>
      <VersionDialog setVersion={setVersion} />
      <Fade cascade damping={0.1}>
        <WelcomeMessage />
      </Fade>
      <Fade cascade delay={200}>
        <About />
      </Fade>
      <Fade cascade delay={400}>
        <FeatureCards />
      </Fade>
      <Fade cascade delay={500}>
        <TOS handleLogin={handleLogin} />
      </Fade>
    </Box>
  );
};

export default Home;
