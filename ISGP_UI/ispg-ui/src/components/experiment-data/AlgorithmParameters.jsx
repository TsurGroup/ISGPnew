import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';


import { FormProvider, useForm } from '../../contexts/FormContext';
import AlgorithmParametersService from '../../services/AlgorithimParametersService';
import AlgoritmParametersForm from './AlgoritmParametersForm';
import DataGraphs from './DataGraphs';

const commonStyles = {
  paddingTop: '30px',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  alignItems: 'flex-start',
  gap: '10px',
  width: '100%',
};

const buttonStyle = {
  position: 'absolute',
  bottom: '15px',
  right: '30px',
  width: '10%',
};

const AlgorithmParameters = () => {
  const [data, setData] = useState({ realImpedanceGraph: { dataset1: [], dataset2: [] }, imaginaryImpedanceGraph: { dataset1: [], dataset2: [] } });
  const [experimentDataForm, setExperimentDataForm] = useState(null);
  //const navigate = useNavigate();

  // Fetch data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const experimentData = await AlgorithmParametersService.getExperimentData();
        setData(experimentData);
        const algorithmParameters = await AlgorithmParametersService.getAlgorithmParameters();
        console.log(algorithmParameters)
        setExperimentDataForm(algorithmParameters);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  if (!experimentDataForm) {
    return <div>Loading...</div>;
  }

  return (
    <Box style={commonStyles}>
      <Box sx={{ flex: 0.75 }}>
        <FormProvider initialFormData={experimentDataForm}>
          {/* <InnerForm /> */}
          <AlgoritmParametersForm />
        </FormProvider>
      </Box>
      <Box sx={{ flex: 0.2 }}>
        <DataGraphs data={data} />
      </Box>
      {/* <Button onClick={saveUserParameters} style={buttonStyle}>
        Save
      </Button> */}
    </Box>
  );
};

// InnerForm Component that watches for changes in form data
// const InnerForm = () => {
//   const { formData, setFormData } = useForm();

//   useEffect(() => {
//     if (formData) {
//       const newRemoveProbability = 1 - (parseFloat(formData.addProbability || 0) + parseFloat(formData.mutateProbability || 0));
      
//       if(parseFloat(formData.addProbability || 0)+parseFloat(formData.mutateProbability || 0) > 1)
//       {
//         const newAddProbability  = formData.addProbability
//       }
        
        
//       // Round the result to 2 decimal places
//       const roundedRemoveProbability = parseFloat(newRemoveProbability.toFixed(2));

//       setFormData((prevData) => ({
//         ...prevData,
//         removeProbability: roundedRemoveProbability,
//       }));
//     }
//   }, [formData.addProbability, formData.mutateProbability, setFormData]);
//   return <ExperimentDataForm />;
// };

export default AlgorithmParameters;
