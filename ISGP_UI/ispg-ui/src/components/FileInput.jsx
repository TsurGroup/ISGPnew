import * as React from 'react';
import { styled } from '@mui/material/styles';
import { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Fab from '@mui/material/Fab';
import DriveFolderUploadRoundedIcon from '@mui/icons-material/DriveFolderUploadRounded';

const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  gap: '15px',
 // minWidth: 'fit-content',
};

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 3,
});

const FileInput = ({ label, name, onFileChange }) => {
  const [fileName, setFileName] = useState(label);

  const handleFileSelection = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onFileChange(e); // Update the form context
    }
  };

  return (
    <Box style={commonStyles}>
      <TextField label={fileName} variant="outlined" disabled sx={{ width: '300px' }} />
      <Fab component="label" variant="contained" color="primary" style={{ padding: '25px', boxShadow: 'none' }} size="small">
        <DriveFolderUploadRoundedIcon fontSize="small" />
        <VisuallyHiddenInput name={name} type="file" accept=".txt,.xlsx" onChange={handleFileSelection} />
      </Fab>
    </Box>
  );
};

export default FileInput;
