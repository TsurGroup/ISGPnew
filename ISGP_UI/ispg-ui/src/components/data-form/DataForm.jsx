import FormInput from './FormInput';
import KKTFormBox from './KKTFormBox';
import SigmoidFilter from './SigmoidFilter';
import KKTGraphs from './KKTGraphs';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DataSetService from '../../services/DataSetService';
import { useForm } from '../../contexts/FormContext';
import FileGuidelines from './FileGuidelines';

const commonStyles = {
  paddingTop: '1%',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  gap: '5%',
  width: '100%',
  paddingLeft: '2%',
  paddingRight: '2%',
  boxSizing: 'border-box',
};

const leftBlockStyles = {
  width: '48%',
  padding: '0 10px',
  display: 'flex',
  flexDirection: 'column',
  gap:'10px'
};

const rightBlockStyles = {
  width: '48%',
  padding: '0 10px',
  display: 'flex',
  flexDirection: 'column',
  //alignItems: 'flex-start',
  gap: '15px',
};


const graphBox = {
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
  position: 'relative',
};

const buttonStyle = {
  textTransform: 'none',
  width: 'auto',
  alignSelf: 'flex-end',
  marginLeft: 'auto',
  marginTop: '20px',
};

const DataForm = () => {
  const navigate = useNavigate();
  const [loadingData, setLoadingData] = useState(false);
  const [dataUploaded, setDataUploaded] = useState(false);
  const [error, setError] = useState(null);

  const initialGraphState = {
    realToImaginaryGraph: { kkTransform: [], realImpedance: [] },
    imaginaryToRealGraph: { kkTransform: [], imaginaryImpedance: [], filteredData: [] },
    coleColeGraph: { kkTransform: [], coleCole: [] },
  };

  const [KKTGraph1, setKKTGraph1] = useState(initialGraphState);
  const [KKTGraph2, setKKTGraph2] = useState(initialGraphState);

  const { formData } = useForm();

  const setFilteredData = (newFilteredData) => {
    setKKTGraph1((prev) => ({
      ...prev,
      imaginaryToRealGraph: { ...prev.imaginaryToRealGraph, filteredData: newFilteredData },
    }));

    setKKTGraph2((prev) => ({
      ...prev,
      imaginaryToRealGraph: { ...prev.imaginaryToRealGraph, filteredData: newFilteredData },
    }));
  };

  const fetchData = async (event) => {
    event.preventDefault();
    setLoadingData(true);
    setError(null);

    const formPayload = new FormData();
    if (formData.file1) formPayload.append('file1', formData.file1[0]);
    if (formData.file2) formPayload.append('file2', formData.file2[0]);
    if (formData.w0) formPayload.append('w0', formData.w0);
    if (formData.w1) formPayload.append('w1', formData.w1);
    formPayload.append('useFilter', formData.useFilter ? 'true' : 'false');

    try {
      const data = await DataSetService.SaveExperimentData(formPayload);
      setKKTGraph1(data[0]);
      setKKTGraph2(data[1]);
      setDataUploaded(true);
    } catch (err) {
      setError('Error uploading data. Please try again.');
      console.error('Error uploading data:', err);
    } finally {
      setLoadingData(false);
    }
  };

  const nextPage = () => {
    navigate('/AlgorithmParameters');
  };

  return (
    <Box sx={commonStyles}>
      <form onSubmit={fetchData}>
          <Box style={leftBlockStyles}>
          <FormInput error={error} loadingData ={loadingData} dataUploaded={dataUploaded} />
           {dataUploaded && <SigmoidFilter setFilteredData={setFilteredData} />}
           </Box>
      </form>
        
      

      <Box style={rightBlockStyles}>
        {dataUploaded ? (    <>
            <KKTGraphs KKTGraph1={KKTGraph1} KKTGraph2={KKTGraph2} />
            <Button sx={buttonStyle} variant="contained" onClick={nextPage}>Continue</Button>
          </>
        ) : (
          <FileGuidelines />
        )}
      </Box>
    </Box>
  );
};

export default DataForm;
