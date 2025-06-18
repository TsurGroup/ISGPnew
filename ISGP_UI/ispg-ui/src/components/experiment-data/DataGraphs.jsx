import Box from '@mui/material/Box';
import GenericGraph from '../global/GenericGraph.jsx'
import { AssignmentReturnOutlined } from '@mui/icons-material';
import { useLocation } from "react-router-dom";

// const salesData = Array.from({ length: 160 }, (_, i) => ({
//     xValue: i + 1,
//     y1Value: Math.floor(Math.random() * 1000),
//     y2Value: Math.floor(Math.random() * 1000),
//   }));
  
//   const temperatureData = Array.from({ length: 160 }, (_, i) => ({
//     xValue: i + 1,
//     y1Value: (Math.random() * 30 + 10).toFixed(2),
//     y2Value: (Math.random() * 30 + 10).toFixed(2),
//   }));

 const commonStyles = {
     //top:'120px',
     display:'flex',
     flexDirection: 'column',
     justifyContent: 'center',
     alignItems: 'center',
     gap: '15px',
    // position:'relative',
    // margin: '0',
    // paddingLeft:'20px',
    width:'100%'
     
   };

const DataGraphs = ({data})=> {
    //const state  = useLocation();
    //const data = state.state.data;
   // console.log(data);

  //   const config = {
  //     dataset1: { label: 'Data set 1', color: '#ff6384', pointRadius: 2, showLine: true },
  //     dataset2: { label: 'Data set 2', color: '#36a2eb', pointRadius: 2,showLine: true },
      
  // };

  const config = {
    xScaleType: 'logarithmic',
    xAxisTitle:'w',
    yAxisTitle:"Z'",
    dataset1: { label: 'Data set 1', color: '#37bd79', pointRadius: 2, showLine: true},
    dataset2: { label: 'Data set 2', color: '#308fac', pointRadius: 2,showLine:true },
    
};

const config2 = {
  xScaleType: 'logarithmic',
  xAxisTitle:'w',
  yAxisTitle:"-Z''",
  dataset1: { label: 'Data set 1', color: '#37bd79', pointRadius: 2, showLine: true},
  dataset2: { label: 'Data set 2', color: '#308fac', pointRadius: 2,showLine:true },
  
};

   return (
        <Box style={commonStyles}>
           {/* <Graph data={data.realImpedance}/>
           <Graph data={data.imaginaryImpedance}/> */}
            <GenericGraph data={data.realImpedanceGraph} config={config} />
            <GenericGraph data={data.imaginaryImpedanceGraph} config={config2} />
           {/* <Graph data={salesData}/>
           <Graph data={temperatureData}/> */}
        </Box>
  
      );
  }
  
  export default DataGraphs;