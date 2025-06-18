import * as React from 'react';
import FileInput from '../FileInput.jsx';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';  
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import { useForm } from '../../contexts/FormContext';

const buttonStyle = {
  textTransform: 'none',
  width: 'auto',
  alignSelf: 'flex-end',
  marginLeft: 'auto',
  marginTop: '20px',
};


const FormInput = ({error,loadingData,dataUploaded}) => {     
  const { handleFileChange } = useForm();

  return (
    <Box component="fieldset" sx={{ p: 2, display: 'flex',flexDirection: 'column', justifyContent: 'center', gap: 2,borderRadius: 2}} >
       <Typography variant="h6" component="legend">Load Data</Typography>
       <Box sx={{display: 'flex',flexDirection: 'column', gap: '24px'}}>
         <FileInput label="Data Set 1" name="file1" onFileChange={handleFileChange} />
         <FileInput label="Data Set 2" name="file2" onFileChange={handleFileChange} />
       </Box>
      <Button type="submit" sx={buttonStyle} variant="contained" disabled={loadingData||dataUploaded}>
             {loadingData ? <CircularProgress size={20} /> : 'Upload Data'}
       </Button>
           {error && <p style={{ color: 'red' }}>{error}</p>}
    </Box>
  );
}

export default FormInput;
