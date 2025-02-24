import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import { Select, MenuItem, FormControl, InputLabel, CircularProgress } from '@mui/material';
import LoadDataService from '../../../services/LoadDataService.js';

const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
  gap: '45px',
  position: 'relative',
  width: '75%'
};

const GenomeSelector = ({ setData }) => {
  const [totalRuns, setTotalRuns] = useState(3);
  const [totalGenerations, setTotalGenerations] = useState(50);
  const [run, setRun] = useState(1);
  const [generation, setGeneration] = useState(1);
  const [fitnessData, setFitnessData] = useState({});
  const [selectedId, setSelectedId] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // Added loading state

  // Fetch total runs
  useEffect(() => {
    const fetchTotalRuns = async () => {
      try {
        const res = await LoadDataService.getRunNum();
        setTotalRuns(res);
      } catch (error) {
        console.error('Error fetching total runs:', error);
      }
    };
    fetchTotalRuns();
  }, []);

  // Fetch total generations based on selected run
  useEffect(() => {
    const fetchRunGenerationNum = async () => {
      try {
        const res = await LoadDataService.getRunsGenerationNum(run);
        setTotalGenerations(res);
      } catch (error) {
        console.error('Error fetching total generations:', error);
      }
    };
    fetchRunGenerationNum();
  }, [run]);

  // Fetch genomes based on selected run and generation
  useEffect(() => {
    const fetchGenomes = async () => {
      try {
        setIsLoading(true); // Start loading
        const res = await LoadDataService.getGenerationModels(run, generation);
        setFitnessData(res);

        // Automatically set the first genome ID as the selected one
        if (res && Object.keys(res).length > 0) {
          const firstGenomeId = Object.keys(res)[0];
          setSelectedId(firstGenomeId);
        }
      } catch (error) {
        console.error('Error fetching genomes:', error);
      } finally {
        setIsLoading(false); // End loading
      }
    };
    fetchGenomes();
  }, [generation, run]);

  // Fetch genome data when selectedId changes
  useEffect(() => {
    const fetchGenomeData = async () => {
      if (selectedId) {
        try {
          const genomeData = await LoadDataService.getModel(selectedId);
          setData(genomeData); // Send genome data to parent
        } catch (error) {
          console.error('Error fetching genome data:', error);
        }
      }
    };
    fetchGenomeData();
  }, [selectedId, setData]);

  // Handle model selection
  const selectModel = (event) => {
    const newSelectedId = event.target.value;
    setSelectedId(newSelectedId);
  };

  // Handle run selection
  const SelectRun = (event) => {
    const selectedRun = event.target.value;
    setRun(selectedRun);
  };

  // Handle generation selection
  const SelectGeneration = (event) => {
    const selectedGeneration = event.target.value;
    setGeneration(selectedGeneration);
  };

  return (
    <Box style={commonStyles}>
      <FormControl fullWidth>
        <InputLabel>Run</InputLabel>
        <Select value={run} onChange={SelectRun} label="Select a Number">
          {Array.from({ length: totalRuns }, (_, i) => (
            <MenuItem key={i + 1} value={i + 1}>
              {i + 1}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl fullWidth>
        <InputLabel>Generation</InputLabel>
        <Select value={generation} onChange={SelectGeneration} label="Select a Number">
          {Array.from({ length: totalGenerations }, (_, i) => (
            <MenuItem key={i + 1} value={i + 1}>
              {i + 1}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl fullWidth>
  <InputLabel>Select Model</InputLabel>
  <Select
    value={selectedId || ""}  // Ensure the value is either the selectedId or an empty string
    onChange={selectModel}
    displayEmpty
    label="Select Model"
  >
    <MenuItem value="" disabled>
      Select Model
    </MenuItem>
    {isLoading ? (
      <MenuItem disabled>
        <CircularProgress size={24} />
      </MenuItem>
    ) : (
      Object.entries(fitnessData).map(([id, fitness], index) => (
        <MenuItem key={id} value={id}>
          {index === 0 ? `Best Model - Fitness: ${fitness}` : `Fitness: ${fitness}`}
        </MenuItem>
      ))
    )}
  </Select>
</FormControl>
    </Box>
  );
};

export default GenomeSelector;
