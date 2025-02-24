import Box from '@mui/material/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';

import NumberField from '../global/NumberField';

import {useForm } from '../../contexts/FormContext';

import DataSetService from '../../services/DataSetService.js'

var Latex = require('react-latex');

const commonStyles = {
    display:'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
    border: '1px solid black',
    borderRadius: '10px',
    //alignItems: 'center',
    //gap: '15px',
    position:'relative',
    //width: '20%',
  };
  const buttonContainerStyles = {
    marginTop: 'auto', // Pushes the button to the bottom
    display: 'flex',
    justifyContent: 'flex-end',
  };
  const a = '$$\\frac{1}{1+e^{-5 \\cdot\\frac{\\log(\\frac{w}{w_0})}{\\log(\\frac{w_1}{w_0})}}}$$'
  const b = '$$\\frac{1}{2}$$' 



const SigmoidFilter = ({setFilteredData,dataUploaded}) =>{     
  const { formData,handleChange } = useForm();
  

    const getFilteredData = async () => {
        try {
          const res = await DataSetService.getFilteredData(formData['w0'],formData['w1']);
          console.log(res.filteredData);
          setFilteredData(res.filteredData);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };


    return (
      <Box 
      component="fieldset" 
      sx={{
        //p: 3,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        //gap: 2.5,
        borderRadius: 2,
      //  width: '500px',  
      }}>
            <legend>Sigmoid Filter</legend> 
             <FormControlLabel control={<Checkbox checked={formData['useFilter']} onChange={() => handleChange({ target: { name:'useFilter', value: !formData['useFilter'] }})}/>} label="use filter" /> 
             <NumberField name={'w0'} defaultValue = {0.25} minValue={0} maxValue={5000} increment={0.01} label={'w0'}/>
             <NumberField name={'w1'}  defaultValue = {0.25} minValue={0} maxValue={5000} increment={0.01} label={'w1'}/> 
             <Box style={buttonContainerStyles}>
             <Button variant="contained"  size="small" disabled={!formData['useFilter'] || !dataUploaded}  onClick ={getFilteredData}>Show Filter</Button>
             </Box>
         </Box>
        
    )
    
}

export default SigmoidFilter;