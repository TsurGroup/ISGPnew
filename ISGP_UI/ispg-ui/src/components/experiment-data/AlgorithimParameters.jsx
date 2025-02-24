import React, { useEffect } from 'react';
import Box from '@mui/material/Box';
import NumberField from '../global/NumberField';


import { useForm } from '../../contexts/FormContext';


const commonStyles = {
    padding: '20px',
    display:'flex',
    flexDirection:'column',
    border: '1px solid black',
    borderRadius: '10px',
    margin: '0',
    //marginTop: '20px',
    //gap:'20px',
    //overflow: 'auto',
    justifyContent: 'center',
    //maxHeight: '450px',
    width:'100%'
  };


const AlgorithimParameters = () => {     
  const { formData, setFormData } = useForm();

  useEffect(() => {
    if (formData) {
      const newRemoveProbability = 1 - (parseFloat(formData.addProbability || 0) + parseFloat(formData.mutateProbability || 0));

      const roundedRemoveProbability = parseFloat(newRemoveProbability.toFixed(2));

      setFormData((prevData) => ({
        ...prevData,
        removeProbability: roundedRemoveProbability,
      }));
    }
  }, [formData.addProbability, formData.mutateProbability, setFormData]);

    return (

        <Box component="fieldset" style={commonStyles}>
        <legend>Algorithim Parameters</legend>
        <Box style={{ maxHeight: '450px', overflow: 'auto', marginTop: '10px'}}>
        <NumberField name="runsNum" minValue={1} maxValue={5} increment={1} label="Number of runs" />
        <NumberField name="maxGenerations"  minValue={1} maxValue={200} increment={1} label="Max number of generations" />
        <NumberField name="expectedPeaksNum"  minValue={1} maxValue={10} increment={1}  label="Expected Number of Peaks"/>
        <NumberField name="mutateProbability"  minValue={0} maxValue={1-formData.addProbability} increment={0.05} label="Mutate peak probability"  />
        <NumberField name="addProbability"  minValue={0} maxValue={1-formData.mutateProbability} increment={0.05} label="Add peak probability" />
        <NumberField name="removeProbability"  minValue={0} maxValue={1} increment={0.05} label="Remove peak probability" disabled={true}/>
        <NumberField name="stopCriteria"   minValue={2} maxValue={20} increment={1} label="Stop criterion" toolTip="number of generations with no improvment"/>
        <NumberField name="duplicationFactor"   minValue={2} maxValue={20} increment={1} label="Duplication factor" toolTip="number of"/>
        
        </Box>
      </Box>
     
    ) 
}
export default AlgorithimParameters;


{/* <label> Number of runs: </label> */}




