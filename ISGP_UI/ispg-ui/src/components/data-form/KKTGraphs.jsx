import * as React from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import GenericGraph from '../global/GenericGraph.jsx';

const commonStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '40px',
};

// Styles for the scrollable content area
const scrollableContentStyles = {
  maxHeight: 'calc(100vh - 300px)', // Adjust height as needed
  overflowY: 'auto',
  padding: '16px', 
  maxWidth: '100%'// Optional: add padding for aesthetics
};

const KKTGraphs = ({ KKTGraph1, KKTGraph2 }) => {
  const [dataSetId, setDataSetId] = useState('1');

  const handleChange = (event, newValue) => {
    setDataSetId(newValue);
  };

  const realToImaginaryGraphConfig = {
    xScaleType: 'logarithmic',
    xAxisTitle: "w",
    yAxisTitle: "Z'",
    kkTransform: { label: 'KKT', color: '#37bd79', pointRadius: 2, showLine: true },
    realImpedance: { label: 'Real Impedance', color: '#308fac', pointRadius: 2, showLine: true },
  };

  const imaginaryToRealGraphConfig = {
    xScaleType: 'logarithmic',
    xAxisTitle: "w",
    yAxisTitle: "Z'",
    kkTransform: { label: 'KKT', color: '#37bd79', pointRadius: 2, showLine: true },
    imaginaryImpedance: { label: 'Imaginary Impedance', color: '#308fac', pointRadius: 2, showLine: true },
    filteredData: { label: 'Filtered Data', color: '#D8F15A', pointRadius: 2, showLine: true },
  };

  const coleColeGraphConfig = {
    
    xAxisTitle: "w",
    yAxisTitle: "Z'",
    kkTransform: { label: 'Data set', color: '#37bd79', pointRadius: 2, showLine: true },
    coleCole: { label: 'KK Transform', color: '#308fac', pointRadius: 2, showLine: true },
  };

  return (
    <Box>
      <Box sx={{ borderBottom: 1, borderColor: 'divider',maxWidth: '100%' }}>
        <Tabs value={dataSetId} onChange={handleChange} aria-label="KKT graphs tabs">
          <Tab label="Data Set 1" value="1" />
          <Tab label="Data Set 2" value="2" />
        </Tabs>
      </Box>
      <Box sx={scrollableContentStyles}>
        {dataSetId === '1' && (
          <Box sx={commonStyles}>
            <GenericGraph data={KKTGraph1.realToImaginaryGraph} config={realToImaginaryGraphConfig} />
            <GenericGraph data={KKTGraph1.imaginaryToRealGraph} config={imaginaryToRealGraphConfig} />
            <GenericGraph data={KKTGraph1.coleColeGraph} config={coleColeGraphConfig} />
          </Box>
        )}
        {dataSetId === '2' && (
          <Box sx={commonStyles}>
             <Box sx={commonStyles}>
            <GenericGraph data={KKTGraph2.realToImaginaryGraph} config={realToImaginaryGraphConfig} />
            <GenericGraph data={KKTGraph2.imaginaryToRealGraph} config={imaginaryToRealGraphConfig} />
            <GenericGraph data={KKTGraph2.coleColeGraph} config={coleColeGraphConfig} />
          </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default KKTGraphs;
