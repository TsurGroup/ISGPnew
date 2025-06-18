import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from '../../contexts/FormContext';

import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Snackbar from '@mui/material/Snackbar';
import SnackbarContent from '@mui/material/SnackbarContent';

import ParametersNavigator from './ParametersNavigator';
import AlgorithimParameters from './AlgorithimParameters';
import PopulationParameters from './PopulationParameters';
import AdvancedParameters from './AdvancedParameters';

import { useProjectState } from '../../contexts/ProjectStateContext';
import AlgorithimParametersService from '../../services/AlgorithimParametersService';

const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'flex-start',
  gap: '15px',
  width: '60%',
  
};

const commonStyles2 = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'flex-start',
  width: '100%',
};

const buttonStyle = {
  position: 'absolute',
  top: '650px',
  right: '30px',
  width: '10%',
};

const AlgoritmParametersForm = () => {
  const navigate = useNavigate();
  const { formData, setFormData } = useForm();
  const [currentFormId, setCurrentFormId] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([0]);  // Track completed steps
  const [buttonDisabled, setButtonDisabled] = useState(true);  // Track if button is disabled
  const [openSnackbar, setOpenSnackbar] = useState(true); // Snackbar open state
  const projectState = useProjectState();

  // Enable button if all forms are completed
  useEffect(() => {
    if (completedSteps.length >= 3) {
      setButtonDisabled(false);  // Enable the button when 3 steps are completed
    } else {
      setButtonDisabled(true);  // Keep it disabled until all steps are completed
    }
  }, [completedSteps]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (buttonDisabled) {
      setOpenSnackbar(true);  // Show Snackbar if button is disabled
      return; // Prevent form submission
    }
    try {
      console.log(formData);
      await AlgorithimParametersService.saveAlgorithmParameters(formData);
      if (projectState.mode === 'create') {
        navigate('/DataDashboard');
      } else {
        navigate('/LoadedDataDashboard');
      }
    } catch (error) {
      console.error('Error saving algorithm parameters:', error);
    }
  };

  const handleNavigate = (index) => {
    if (!completedSteps.includes(index)) {
      setCompletedSteps([...completedSteps, index]);  // Add current form ID to the completed list
    }
    setCurrentFormId(index);
  };

  const handleSnackbarClose = () => {
    setOpenSnackbar(false);  // Close Snackbar after it's shown
  };

  return (
    <Box style={commonStyles2}>
      <form onSubmit={handleSubmit}>
        <Box style={commonStyles}>
          <ParametersNavigator
            currentFormId={currentFormId}
            setCurrentFormId={handleNavigate}  // Allow navigating to forms
          />
          {currentFormId === 0 && <AlgorithimParameters />}
          {currentFormId === 1 && <PopulationParameters />}
          {currentFormId === 2 && <AdvancedParameters />}
        </Box>

        {/* "Run" button */}
        <Button
          type="submit"
          sx={buttonStyle}
          variant="contained"
          disabled={buttonDisabled}
        >
          {projectState.mode === 'create' ? 'Run' : 'Load'}
        </Button>
      </form>

      {/* Snackbar Notification */}
      <Snackbar
        open={openSnackbar}
        onClose={handleSnackbarClose}
        autoHideDuration={3000} // Snackbar disappears after 3 seconds
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
      >
        <SnackbarContent
          message="Please browse all parameters in order to proceed"
          sx={{
            backgroundColor: '#37bd79', // Set background color to white
            color: 'white', // Set text color to black
            '& .MuiSnackbarContent-message': {
              fontWeight: 'bold', // Optional: Make the text bold
            },
          }}
        />
      </Snackbar>
    </Box>
  );
};

export default AlgoritmParametersForm;
