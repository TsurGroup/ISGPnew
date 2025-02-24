import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import PauseIcon from '@mui/icons-material/Pause';
import StopCircleIcon from '@mui/icons-material/StopCircle';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import Timer from '../global/Timer';
import AbortDialog from './AbortDialog'
import { abortEvolution } from '../../services/DashboardService';


const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '25px',
  width:'100%',
};

const commonStyles2 = {
  position: 'fixed',
  bottom: 0,
  right: 0,
  padding: '10px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'flex-end',
  gap: '10px',
  width: '20%', // Set a width for the container
};

const buttonStyle = {
  width: '150px', // Make the buttons flexible
};

const DashboardControls = ({isPaused,setIsPaused,startTime}) => {
  //const [isPaused, setIsPaused] = useState(false);
  const [open, setOpen] = useState(false);
  //const [startTime] = useState(Date.now());

  const handleButtonClick = () => {
   setIsPaused((prevIsPaused) => !prevIsPaused);
  };

  const openAbortDialog = async () => {
    setOpen(true);
  };

  return (
    <Box sx={commonStyles2}>
      <Timer startTime={startTime} isPaused={isPaused} style={buttonStyle} />
      <Box sx={commonStyles}>
        <Button sx={buttonStyle} variant="contained" color="primary" onClick={handleButtonClick} startIcon={isPaused ? <PlayCircleIcon /> : <PauseIcon />}>
          {isPaused ? 'Start' : 'Pause'}
        </Button>
        <Button sx={buttonStyle} color="primary" variant="contained" onClick={openAbortDialog} startIcon={<StopCircleIcon />}>Abort</Button>
        <AbortDialog open = {open} setOpen ={setOpen} setIsPaused={setIsPaused}/>
      </Box>
    </Box>
  );
};

export default DashboardControls;