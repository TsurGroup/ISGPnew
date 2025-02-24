import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Box from '@mui/material/Box';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';

import { useSetProjectState } from '../../../contexts/ProjectStateContext';

import HomeService from '../../../services/HomeService';


const CreateProjectDialog = ({ open, onClose}) => {

const [newProjectName, setNewProjectName] = useState('');
const [error, setError] = useState('');

const navigate = useNavigate();
const setProjectState = useSetProjectState();

const handleClose = () => {
    setNewProjectName('');
    setError(''); // Clear error message when the user changes input
    onClose();
  };


const handleInputChange = (e) => {
    setNewProjectName(e.target.value);
    setError(''); // Clear error message when the user changes input
  };

const createNewProject = async () => {
    if (newProjectName.trim() === '') {
      alert('Project name cannot be empty');
      return;
    }
    try {
      await HomeService.createProject(newProjectName);
      setProjectState({ mode:'create'});
      handleClose();
      navigate('/Data');
    } catch (error) {
      console.error('Error creating project:', error);
      setError(error.message);
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth>
      <DialogTitle>Create Project</DialogTitle>
      <DialogContent>
        <Box sx={ {display:'flex',flexDirection: 'column',gap:'10px',padding:'10px'}}>
        <TextField label="Project Name" variant="outlined" value={newProjectName} onChange={(e) => handleInputChange(e)}  fullWidth />
        {<Alert sx={{ mt: 1, visibility: error ? 'visible' : 'hidden' }} severity="error">{error}</Alert>}
        </Box>
      </DialogContent>
      <DialogActions>

        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={createNewProject} disabled={!newProjectName.trim()}>Create Project</Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateProjectDialog;
