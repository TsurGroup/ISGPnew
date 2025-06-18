import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';  

import NumberField from '../global/NumberField';
import { useForm } from '../../contexts/FormContext';
import DataSetService from '../../services/DataSetService.js';

const commonStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'flex-start',
  border: '1px solid black',
  borderRadius: '10px',
  position: 'relative',
};

const buttonStyle = {
  textTransform: 'none',
  width: 'auto',
  alignSelf: 'flex-end',
  marginLeft: 'auto',
  marginTop: '20px',
};


const SigmoidFilter = ({ setFilteredData }) => {
  const { formData, handleChange } = useForm();
  const [loading, setLoading] = useState(false); // Track loading state

  // Function to trigger the setFilter logic
  const setFilter = async () => {
    setLoading(true); // Show loading spinner when the request is made
    const filterData = {
      w0: formData['w0'],
      w1: formData['w1'],
      useFilter: formData['useFilter'],
    };

    try {
      const res = await DataSetService.setFilter(filterData); // Send POST request with data in the body
      console.log(res.success); // Handle the response, if necessary
      setFilteredData(res.filteredData); // Update the filtered data
    } catch (error) {
      console.error('Error setting filter:', error);
    } finally {
      setLoading(false); // Hide loading spinner once the request is complete
    }
  };

  useEffect(() => {
    // This will run whenever formData['useFilter'] changes
    setFilter();
  }, [formData['useFilter']]); // Trigger effect when 'useFilter' changes
  
  const handleCheckboxChange = (event) => {
    // Directly toggle 'useFilter'
    handleChange({ target: { name: 'useFilter', value: !formData['useFilter'] } });
  };

  return (
    <Box component="fieldset" sx={{ p:2,display: 'flex', flexDirection: 'column', justifyContent: 'center', borderRadius: 2 ,gap:1}}>
      <Typography variant="h6" component="legend"> Sigmoid Filter </Typography>
      <Box sx={{display: 'flex',flexDirection: 'column', gap: '1px'}}>
        <FormControlLabel sx = {{paddingLeft:'10px'}}control={<Checkbox checked={formData['useFilter']} onChange={handleCheckboxChange} />} label="Use Filter" />
        <NumberField name={'w0'} defaultValue={0.25} minValue={0} maxValue={5000} increment={0.01} label={'w0'} />
        <NumberField name={'w1'} defaultValue={0.25} minValue={0} maxValue={5000} increment={0.01} label={'w1'} />
      </Box>
  
        <Button sx={buttonStyle} variant="contained"  disabled={loading || !formData['useFilter']} onClick={setFilter}>
          Show Filter
        </Button>
  
    </Box>
  );
};

export default SigmoidFilter;
