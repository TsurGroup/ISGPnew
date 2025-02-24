import Box from '@mui/material/Box';
import GenericGraph from '../global/GenericGraph.jsx'

 const commonStyles = {
     //top:'120px',
     display:'flex',
     flexDirection: 'row',
     justifyContent: 'center',
     alignItems: 'center',
     gap: '40px',
     position:'relative',
     margin: '0',
     flexWrap: 'wrap'
     
   };

   const impedanceGraphconfig = {
    xAxisTitle:"Z",
    yAxisTitle:"-Z''",
    dataset1: { label: 'Dataset 1', color: '#0457ac', pointRadius: 2, showLine: true },
    dataset2: { label: 'Dataset 2', color: '#308fac', pointRadius: 2,showLine: true },
    model: { label: 'Model', color: '#37bd79', pointRadius: 2,showLine: true }
    
};

const modelGraphconfig = {
  xAxisTitle:"log_10(t)",
  yAxisTitle:"",
  model: { label: 'Model', color: '#37bd79', pointRadius: 2, showLine: true },
  
};

const residualGraphconfig = {
  xAxisTitle:"log_10(t)",
  yAxisTitle:"Residual",
  dataset1: { label: 'Dataset 1', color: '#0457ac', pointRadius: 2, showLine: true },
  dataset2: { label: 'Dataset 2', color: '#308fac', pointRadius: 2,showLine: true },
  
};

const discrepancyGraphconfig = {
  //yScaleType:'logarithmic',
  xAxisTitle:"Complexity",
  yAxisTitle:"Discrepancy",
  currentModel:{ label: 'Best model', color: '#37bd79', pointRadius: 7,showLine: false,pointStyle:'rectRot' },
  bestModels: { label: 'Best models', color: '#0457ac', pointRadius: 5,showLine: false,pointStyle:'triangle' },
  allDiscrepancies: { label: 'All models', color: '#f4e604', pointRadius: 2, showLine: false },
  
  
};

const DashboardGraphs = ({SolutionGraphData,ResidualGraphData,ImpedanceGraphDataConst,DiscrepancyGraphData})=> {
    //  const state  = useLocation();
    //  const data = state.state.data;
   return (
        <Box style={commonStyles}>
           
            <GenericGraph data={ImpedanceGraphDataConst} config={impedanceGraphconfig} />
            <GenericGraph data={SolutionGraphData} config={modelGraphconfig} />
            <GenericGraph data={ResidualGraphData} config={residualGraphconfig} />
            <GenericGraph data={DiscrepancyGraphData} config={discrepancyGraphconfig} />

        </Box>
  
      );
  }
  
  export default DashboardGraphs;