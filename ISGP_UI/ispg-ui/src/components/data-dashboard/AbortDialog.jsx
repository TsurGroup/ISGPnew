import React, { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import CircularProgress from '@mui/material/CircularProgress';
import { abortEvolution } from '../../services/DashboardService';




const AbortDialog = ({open,setOpen,setIsPaused}) => {
    const [isAborting, setIsAborting] = useState(false);
      const handleClose = () => {
        setOpen(false);
      };

  const handleAbort = async () => {
    try {
      setIsAborting(true);
      const responseData = await abortEvolution();
      console.log(responseData);

      setIsPaused(true);
      setOpen(false);
      setIsAborting(false);
      
    } catch (error) {
      console.error('Error aborting evolution:', error);
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description">
    <DialogTitle id="alert-dialog-title"> {"Abort"} </DialogTitle>
    <DialogContent>
      <DialogContentText id="alert-dialog-description">
     Are you sure you want to stop running evolution? 
      </DialogContentText>
    </DialogContent>
    <DialogActions>
      <Button onClick={handleClose}>No</Button>
      <Button onClick={handleAbort} autoFocus> Yes </Button>
      {isAborting && <CircularProgress /> }
    </DialogActions>
  </Dialog>
  );
};

export default AbortDialog;