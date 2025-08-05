import React from 'react';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Box from '@mui/material/Box';

import Latex from 'react-latex';
// import 'katex/dist/katex.min.css';

import GenerationDataGrid from './GenerationDataGrid'
import DashboardGraphs from './DashboardGraphs'
import ConfirmNavigationDialog from './ConfirmNavigationDialog'
import DashboardControls from './DashboardControls'

import { abortEvolution } from '../../services/DashboardService';
import { createEventSource,connectToEvolution,closeEvolutionSocket } from '../../services/DashboardService';

import useNavigationBlocker from '../../hooks/useNavigationBlocker';



//var Latex = require('react-latex');

const commonStyles = {
  top:'20px',
  display:'flex',
  flexDirection: 'row',
  //justifyContent: 'center',
  alignItems: 'center',
  gap: '45px',
  position:'relative',
  flexWrap: 'wrap',
  //maxHeight: '100vh', /* or height: 100vh; */
 // overflow: 'auto',/* or overflow-y: auto; */
  //boxSizing: 'border-box'
};

const commonStyles2 = {
  //top:'20px',
  display:'flex',
  flexDirection: 'row',
  //justifyContent: 'center',
  alignItems: 'center',
  gap: '35px',
  position:'relative',
  //flexWrap: 'wrap',
  maxHeight: '100vh',
  width:'100%' /* or height: 100vh; */
 // overflow: 'auto',/* or overflow-y: auto; */
 // boxSizing: 'border-box'
};

const commonStyles3 = {
  overflowWrap: 'break-word', 
  whiteSpace: 'normal',
  wordWrap: 'break-word',
  width: '100%', // Ensure the box takes the full width available
  maxWidth: '100%', // Prevent the box from exceeding the container width
  overflow: 'hidden' // Ensure the box takes the full width available
};


  
const DataDashboard = () => {
const [data, setData] = useState(
      {impadanceGraphView:{dataset1:[],dataset2:[],model: []},impedanceGraph:[],modelGraph :{model:[]},
      residualGraph:{dataset1:[],dataset2:[]},run:1,fitness:null,area:null,generation:null,modelString:'$$',
      discrepancyGraph:{currentModel:[],bestModels:[],allDiscrepancies:[],}});
const [isPaused, setIsPaused] = useState(false);
const [startTime] = useState(Date.now()); // Set initial start time
const [open, setOpen] = useNavigationBlocker();
const [isCompleted, setIsCompleted] = useState(false);
const navigate = useNavigate();

// useEffect(() => {
//   const handleNewEvents = (eventData) => {
//     setData(eventData);
//   };

//   const handleError = (error) => {
//     console.error('Error receiving events:', error);
//     setIsPaused(true); // Pause the timer when an error occurs
//   };

//   const handleOpen = () => {
//     setIsPaused(false); // Resume the timer when the connection is opened
//   };

//   const eventSource = createEventSource(handleNewEvents, handleError, handleOpen);

//   eventSource.onclose = () => {
//     console.log('Connection closed');
//     navigate('/CompletionScreen'); // Navigate to the completion screen
//   };

//   return () => {
//     eventSource.close();
//   };
// }, [navigate]);

// useEffect(() => {
//   if(isPaused)
//    {
//     navigate('/CompletionScreen');
//    }
// }, [isPaused]);
      
// useEffect(() => {
//   const handleNewEvents = (eventData) => {
//     setData(eventData);
//   };

//   const handleError = (error) => {
//     console.error('Error receiving events:', error);
//     setIsPaused(true); // Pause the timer when an error occurs
//   };

//   const handleOpen = () => {
//     setIsPaused(false); // Resume the timer when the connection is opened
//   };

//   const handleClose = () => {
//     setIsCompleted(true); // Resume the timer when the connection is opened
//   };

//   const eventSource = createEventSource(handleNewEvents, handleError, handleOpen,handleClose);

//   eventSource.onclose = () => {
//     console.log('Connection closed by the server.');
    
//   };

//   return () => {
//     console.log('Closing EventSource from the frontend.');
//     eventSource.close();
    
//   };
// }, []);

useEffect(() => {
  const handleNewEvents = (incoming) => {
    setData(incoming);
    console.log(incoming);
  };

  const handleSocketClose = () => {
    setIsPaused(true);
    setIsCompleted(true);
    setTimeout(() => navigate('/CompletionScreen'), 50); // ⏱️ give it a tick
  };

  const handleSocketError = (err) => {
    console.log("err is acurring")
    console.log(err)
    setIsPaused(true);
    //alert('A connection error occurred. Please check your connection or try again later.');
  };

  connectToEvolution(
    handleNewEvents,
    handleSocketClose,
    handleSocketError
  );

  return () => {
    console.log("Cleaning up socket")
    setIsPaused(true);
    closeEvolutionSocket(); // 👈 this was killing it early
  };
}, []); // 👈 only run once on mount



const handleClose = () => {
    setOpen(false);
    //window.history.pushState(null, '', window.location.href); // Prevent navigation
  };


  const handleLeave = async () => {
    //console.log(window.history);
   // try {
   //   const responseData = await abortEvolution();
   // } catch (error) {
      
   // }
    
    console.log(window.history);
    setOpen(false);
    //navigate(-1); // Navigate back
  };

    
return (
           
<Box style={commonStyles}>
      <DashboardGraphs SolutionGraphData={data.modelGraph} ResidualGraphData = {data.residualGraph} 
      ImpedanceGraphDataConst={data.impadanceGraphView} DiscrepancyGraphData={data.discrepancyGraph}/>
     
      <Box style={commonStyles2}>
         <GenerationDataGrid props = {{run:data.run,fitness:data.fitness, generation : data.generation,area:data.area}}/>
         <Box sx={commonStyles3}>
         <Latex >{data.modelString}</Latex>
         </Box>
         <DashboardControls isPaused={isPaused} setIsPaused={setIsPaused} startTime={startTime}/>
         <ConfirmNavigationDialog open={open} onClose={handleClose} onLeave={handleLeave} />

      </Box>
     
</Box>

)}
export default DataDashboard;