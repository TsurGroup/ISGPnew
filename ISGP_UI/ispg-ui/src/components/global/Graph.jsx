import React, { PureComponent } from 'react';
import Box from '@mui/material/Box';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';



const Graph = ({data})=> {
    // console.log(data);
    // const graphData = getGraphData(data.data);
    // console.log(graphData);
    // const max = data.data.frequency.reduce((a, b) => { return Math.max(a, b) });
   console.log(data)

 return (
   <LineChart width={500} height={200} data={data} margin={{top: 5,right: 30,left: 20,bottom: 5}}>
      <CartesianGrid strokeDasharray="5 5" />
      <XAxis dataKey='xValue' type="number"/>
      <YAxis />
      <Tooltip />
      <Legend />
        <Line dataKey='y1Value' name='Re Impedance'/> 
        <Line dataKey='y2Value' name='Im Impedance'/> 
      </LineChart>
        
    );
}

export default Graph;



 // const getGraphData = (data) =>
  // {
  //   console.log(data);
  //   const graphData = [];
  //   for (let i = 0; i < data.frequency.length; i++) {
  //     graphData.push({frequency:data.frequency[i],real_electrical_impedance:data.real_electrical_impedance[i],imaginary_electrical_impedance:data.imaginary_electrical_impedance[i]})

  //   }
  //   return graphData;
  // }