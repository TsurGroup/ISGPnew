import * as React from 'react';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import FormControlLabel from '@mui/material/FormControlLabel';

const commonStyles = {
    padding: '5px',
    display:'flex',
    border: '1px solid black',
    justifyContent: 'center',
    //width: '20%',
    borderRadius: '10px',
    //margin: 'auto',
  };


const KKTFormBox = () =>
{     

    return (
           
         <Box component="fieldset" style = {commonStyles}>
         <legend>Kramers-Kronig Transforms (KKT)</legend> 
           <FormControl>
                <FormControlLabel control={<Checkbox defaultChecked />} label="Use KKT" />
           </FormControl>
         </Box>
        
    )
    
}


export default KKTFormBox;