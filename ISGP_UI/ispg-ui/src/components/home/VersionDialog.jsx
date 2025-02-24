import React, { useState, useEffect } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import HomeService from '../../services/HomeService';

const VersionDialog = ({setVersion}) => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState(false);

  useEffect(() => {
    const checkAppVersion = async () => {
      try {
        console.log("am i here");
        const versionInfo = await HomeService.checkVersion();
        console.log(versionInfo);
        setVersion(versionInfo.currentVersion);
        if (versionInfo.updateAvailable) {
          setError(false);
          
          setMessage(versionInfo.message);
          setOpen(true);
        } else {
          console.log("Your application is up to date.");
        }
      } catch (error) {
        console.error(error);
        setError(true);
        setMessage('We\'re having trouble checking for updates right now. Your current version is still valid, and you can continue using the app as usual. Please try again later.');
        setOpen(true);
      }
    };

    checkAppVersion();
  }, []);

  const handleClose = () => {
    setOpen(false);
  };

  const messageLines = message.split('\n');

  return (
    <Dialog open={open} onClose={handleClose} fullWidth>
      <DialogTitle>{error ? 'Verification Failed' : 'Update Available'}</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: '10px', padding: '10px' }}>
          <Alert severity="warning">
            {messageLines.map((line, index) => (
              <div key={index}>{line}</div>
            ))}
          </Alert>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>OK</Button>
      </DialogActions>
    </Dialog>
  );
};

export default VersionDialog;
