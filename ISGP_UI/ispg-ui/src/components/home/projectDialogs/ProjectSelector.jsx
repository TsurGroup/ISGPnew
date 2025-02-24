import React, { useState } from 'react';
//import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CreateProjectDialog from './CreateProjectDialog';
import LoadProjectDialog from './LoadProjectDialog';

const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '15px',
  padding: '10px',
};

const ProjectSelector = ({ agreedToTOS }) => {
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [isLoadingProject, setIsLoadingProject] = useState(false);


  //const navigate = useNavigate();

  const openCreateProjectDialog = () => setIsCreatingProject(true);
  const openLoadProjectDialog = () => setIsLoadingProject(true);

  return (
    <Box sx={commonStyles}>
      <Button disabled={!agreedToTOS} variant="contained" onClick={openCreateProjectDialog}>
        New Project
      </Button>
      <CreateProjectDialog
        open={isCreatingProject}
        onClose={() => setIsCreatingProject(false)}
      />

      <Button disabled={!agreedToTOS} variant="contained" onClick={openLoadProjectDialog}>
        Load Project
      </Button>
      <LoadProjectDialog
        open={isLoadingProject}
        onClose={() => setIsLoadingProject(false)}
      />
    </Box>
  );
};

export default ProjectSelector;
