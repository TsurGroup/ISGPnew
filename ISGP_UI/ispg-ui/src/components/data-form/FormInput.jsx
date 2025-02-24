import * as React from 'react';
import FileInput from '../FileInput.jsx';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';  // Import Typography
import { useForm } from '../../contexts/FormContext';

const FormInput = () => {     
  const { handleFileChange } = useForm();

  return (
    <Box 
      component="fieldset" 
      sx={{
        p: 3,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: 3,
        borderRadius: 2,
      }}
    >
      <Typography variant="h6" component="legend">
        Load Data
      </Typography>
      <FileInput label="Data Set 1" name="file1" onFileChange={handleFileChange} />
      <FileInput label="Data Set 2" name="file2" onFileChange={handleFileChange} />
    </Box>
  );
}

export default FormInput;
