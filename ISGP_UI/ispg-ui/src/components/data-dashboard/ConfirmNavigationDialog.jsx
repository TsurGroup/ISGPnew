import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button } from '@mui/material';

const ConfirmNavigationDialog = ({ open, onClose, onLeave }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Confirm Navigation</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Are you sure you want to leave this page? Any unsaved changes may be lost.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">Stay</Button>
        <Button onClick={onLeave} color="secondary">Leave</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ConfirmNavigationDialog;
