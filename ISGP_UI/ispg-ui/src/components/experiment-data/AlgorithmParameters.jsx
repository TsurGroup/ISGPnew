import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';

import { FormProvider, useForm } from '../../contexts/FormContext';
import AlgorithmParametersService from '../../services/AlgorithimParametersService';
import AlgoritmParametersForm from './AlgoritmParametersForm';
import DataGraphs from './DataGraphs';

const commonStyles = {
  paddingTop: '1%',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between', // This will place the two blocks on opposite sides
  gap: '5%', // Reduced gap to balance the layout and avoid overflow
  width: '100%',
  paddingLeft: '1%', // Adjusting padding
  paddingRight: '2%', // Adjusting padding on the right side as well
  boxSizing: 'border-box', // Ensures that padding is included in the width
};

const leftBlockStyles = {
  width: '56%', // Left block now takes 48% of the width to leave room for the gap
  padding: '0 10px', // Padding on the left and right sides only
};

const rightBlockStyles = {
  width: '40%', // Right block now takes 48% of the width
  padding: '0 10px', // Padding on the left and right sides only
};

const AlgorithmParameters = () => {
  const [data, setData] = useState({ realImpedanceGraph: { dataset1: [], dataset2: [] }, imaginaryImpedanceGraph: { dataset1: [], dataset2: [] } });
  const [experimentDataForm, setExperimentDataForm] = useState(null);

  // Fetch data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const experimentData = await AlgorithmParametersService.getExperimentData();
        setData(experimentData);
        const algorithmParameters = await AlgorithmParametersService.getAlgorithmParameters();
        console.log(algorithmParameters);
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
      <Box style={leftBlockStyles}>
        <FormProvider initialFormData={experimentDataForm}>
          <AlgoritmParametersForm />
        </FormProvider>
      </Box>
      <Box style={rightBlockStyles}>
        <DataGraphs data={data} />
      </Box>
    </Box>
  );
};

export default AlgorithmParameters;
