import * as React from 'react';
import Box from '@mui/material/Box';
import NumberField from '../global/NumberField';



const commonStyles = {
    padding: '20px',
    display:'flex',
    flexDirection:'column',
    border: '1px solid black',
    borderRadius: '10px',
    margin: '0',
    width: '100%',

    justifyContent: 'center',
    //gap:'20px',
    
  };

const AdvancedParameters = () => {     

    return (
         <Box component="fieldset" style = {commonStyles}>
             <legend>Advanced Parameters</legend>
             <NumberField name="normFactor" defaultValue ={0.05} minValue={1} maxValue={5} increment={0.05}  label="Normalization penalty" toolTip="Penalty for not being properly normalized where 0 relates to no penalty"/>
             <NumberField name="pointDiff" defaultValue ={3} minValue={1} maxValue={20} increment={1} label="Point Diff Factor"/>
             <NumberField name="widthFactor" defaultValue ={8} minValue={0} maxValue={45} increment={1} label="Width Factor" toolTip="Penalty on too wide peaks"/>
             <NumberField name="alpha" defaultValue ={0.8} minValue={0} maxValue={1} increment={0.05} label="Alpha"/>
          
            

         </Box>
    ) 
}
export default AdvancedParameters;


{/* <label> Number of runs: </label> */}




