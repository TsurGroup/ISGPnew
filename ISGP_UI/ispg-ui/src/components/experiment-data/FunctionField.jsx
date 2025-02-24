import Box from '@mui/material/Box';
import React, { useState } from 'react';

import FormControlLabel from '@mui/material/FormControlLabel';
import { Grid, Checkbox, Typography } from '@mui/material';

const commonStyles = {
    display:'flex',
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    gap: '15px',
    position:'relative',
    width: '20%',
  };

const FunctionField = ({label}) =>
{     
    const [checked, setChecked] = useState([true, false]);

    const handleCheckboxChange = (index) => {
      const newChecked = [...checked];
      newChecked[index] = !newChecked[index];
      setChecked(newChecked);
    };
    return (
           
        //  <Box  style = {commonStyles}>
        //  {label ? <label style={ {minWidth: '200px'}}> {label}: </label> : null}
        //  <FormControlLabel control={<Checkbox defaultChecked />}  />
        //  <FormControlLabel control={<Checkbox defaultChecked />}/>
        //  {/* <NumberField section="PopulationParameters" name="lb" defaultValue={0.25} minValue={-100} maxValue={100} increment={0.2}  useFormContext={false} />
        //  <NumberField section="PopulationParameters" name="ub" defaultValue={0.25} minValue={-100} maxValue={100} increment={0.2}  useFormContext={false} /> */}
        //  </Box>

        <Grid container spacing={2} alignItems="center">
        <Grid item xs={2.5}>
          <Typography variant="body1">{label}</Typography>
        </Grid>
        {checked.map((isChecked, index) => (
          <Grid item xs={2.5} key={index}>
            <Checkbox
              
            //   onChange={() => handleCheckboxChange(index)}
            />
          </Grid>
        ))}
      </Grid>
        
    )
    
}

export default FunctionField;