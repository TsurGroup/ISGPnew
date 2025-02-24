import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContentText from '@mui/material/DialogContentText';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Alert from '@mui/material/Alert';

import { useSetProjectState } from '../../../contexts/ProjectStateContext';
import HomeService from '../../../services/HomeService';

const LoadProjectDialog = ({ open, onClose }) => {
  const [isLoadingProjects, setIsLoadingProjects] = useState(false);
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [error, setError] = useState(null);

  const navigate = useNavigate();
  const setProjectState = useSetProjectState();

  useEffect(() => {
    if (open) {
      loadProjects();
    }
  }, [open]);

  const loadProjects = async () => {
    setIsLoadingProjects(true);
    setError(null); // Clear previous errors
    try {
      const projectNames = (await HomeService.getProjects()) || [];
      setProjects(projectNames);
    } catch (err) {
      console.error('Error fetching projects:', err);
      setError('Failed to load projects. Please try again.');
    } finally {
      setIsLoadingProjects(false);
    }
  };

  const loadSelectedProject = async () => {
    if (selectedProject) {
      setIsLoadingProjects(true);
      setError(null);
      try {
        await HomeService.loadProject(selectedProject);
        setProjectState({ mode: 'load' });
        navigate('/AlgorithmParameters');
      } catch (err) {
        console.error('Error loading project:', err);
        setError('Failed to load project. Please try again.');
      } finally {
        setIsLoadingProjects(false);
        onClose();
      }
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth>
      <DialogTitle>Load Project</DialogTitle>
      <DialogContent>
        {error && <Alert severity="error">{error}</Alert>}
        {isLoadingProjects ? (
          <DialogContentText>Loading projects...</DialogContentText>
        ) : (
          <List>
            {projects.length > 0 ? (
              projects.map((projectName) => (
                <ListItem
                  button
                  role="button"
                  key={projectName}
                  onClick={() => setSelectedProject(projectName)}
                  selected={selectedProject === projectName}
                >
                  <ListItemText primary={projectName} />
                </ListItem>
              ))
            ) : (
              <DialogContentText>No projects available</DialogContentText>
            )}
          </List>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={loadSelectedProject}
          disabled={!selectedProject || isLoadingProjects}
        >
          {isLoadingProjects ? 'Loading...' : 'Load Project'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default LoadProjectDialog;
