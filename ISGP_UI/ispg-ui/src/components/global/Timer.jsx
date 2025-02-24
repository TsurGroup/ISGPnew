import React, { useState, useEffect, useRef } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const Timer = ({ startTime, isPaused }) => {
  const [elapsedTime, setElapsedTime] = useState(0);
  const [pausedTime, setPausedTime] = useState(0);
  const lastPauseRef = useRef(null);

  const updateElapsedTime = () => {
    const currentTime = Date.now();
    setElapsedTime(currentTime - startTime - pausedTime);
  };

  useEffect(() => {
    let interval;

    if (!isPaused) {
      if (lastPauseRef.current !== null) {
        setPausedTime(prevPausedTime => prevPausedTime + (Date.now() - lastPauseRef.current));
        lastPauseRef.current = null;
      }
      interval = setInterval(updateElapsedTime, 1000);
    } else {
      lastPauseRef.current = Date.now();
      clearInterval(interval);
    }

    return () => clearInterval(interval);
  }, [isPaused, startTime, pausedTime]);

  const hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((elapsedTime / 1000 / 60) % 60);
  const seconds = Math.floor((elapsedTime / 1000) % 60);

  const padTime = (time) => String(time).padStart(2, '0');

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'primary.main',
        color: 'white',
        padding: 1,
        borderRadius: 1,
        width:'100%',
        height:'5%',
        boxSizing: 'border-box'
      }}
    >
      <Typography variant="h5" component="p">
        {padTime(hours)}:{padTime(minutes)}:{padTime(seconds)}
      </Typography>
    </Box>
  );
};

export default Timer;