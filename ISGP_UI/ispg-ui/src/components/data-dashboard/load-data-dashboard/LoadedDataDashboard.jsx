import React from 'react';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import { Select, MenuItem, FormControl, InputLabel, FormHelperText } from '@mui/material';

import Latex from 'react-latex';
// import 'katex/dist/katex.min.css';

import GenerationDataGrid from '../GenerationDataGrid.jsx'
import DashboardGraphs from '../DashboardGraphs.jsx'
import GenomeSelector from './GenomeSelector.jsx'

import LoadDataService from '../../../services/LoadDataService.js'
import DataItem from '../../global/DataItem';
//var Latex = require('react-latex');

const commonStyles = {
//  top:'20px',
  display:'flex',
  flexDirection: 'column',
  //justifyContent: 'center',
  alignItems: 'center',
  gap: '20px',
  position:'relative',
  flexWrap: 'wrap',

};

const commonStyles2 = {
  display:'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  alignItems: 'center',
  gap: '35px',
  position:'relative',
  //flexWrap: 'wrap',
  //maxHeight: '100vh',
  width:'100%' /* or height: 100vh; */
};


const commonStyles3 = {
  overflowWrap: 'break-word', 
  whiteSpace: 'normal',
  wordWrap: 'break-word',
  width: '100%', // Ensure the box takes the full width available
  maxWidth: '100%', // Prevent the box from exceeding the container width
  overflow: 'hidden' // Ensure the box takes the full width available
};

const paginationStyle = {
  display:'flex',
  flexDirection: 'column',

};

  
const LoadedDataDashboard = () => {
    const [data, setData] = useState(
      {impadanceGraphView:{dataset1:[],dataset2:[],model: []},impedanceGraph:[],modelGraph :{model:[]},
      residualGraph:{dataset1:[],dataset2:[]},run:1,fitness:null,area:null,generation:null,modelString:'$$',
      discrepancyGraph:{currentModel:[],bestModels:[],allDiscrepancies:[],}});

      // const [run, setRun] = useState(1);
      // const [generation, setGeneration] = useState(1);
      //const [fitnessData, setFitnessData] = useState({}); // To hold the id and fitness mapping
      //const [selectedId, setSelectedId] = useState(null);

// useEffect(() => {
//     const fetchData = async () => {
//         try {
//           const model = await LoadDataService.getGenerationModel(run,generation);
//           console.log(model)
//           setFitnessData(model);
//         } catch (error) {
//           console.error('Error fetching data:', error);
//         }
//       };
//       fetchData();
// }, [run,generation]);
 // Dependency on selectedId


return (
           
<Box style={commonStyles}>


      <DashboardGraphs SolutionGraphData={data.modelGraph} ResidualGraphData = {data.residualGraph} 
      ImpedanceGraphDataConst={data.impadanceGraphView} DiscrepancyGraphData={data.discrepancyGraph}/>
     
      {/* <Box style={commonStyles2}> */}
          <GenomeSelector setData={setData}/>
        <Box sx={commonStyles2}> 
        <DataItem label={'Model'} value={ <Latex >{data.modelString}</Latex> } />
        <DataItem label={'Area'} value={data.area} />
        </Box> 

      {/* </Box> */}
     
</Box>

)}
export default LoadedDataDashboard;