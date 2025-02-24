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

const outerBoxStyle = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-between',
  //padding: '40px',
  margin: '0 auto',       // Centers the box horizontally
  maxWidth: '90%',     // Limits the maximum width to avoid stretching
  height: '80vh',         // Reduce height to avoid unnecessary scrolling
  boxSizing: 'border-box',
};

const commonStyles = {
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
  width:'500px'
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
    <Box sx={outerBoxStyle}>
      <form onSubmit={fetchData}>
        <Box sx={commonStyles}>
          <FormInput />
          {/* <KKTFormBox /> */}
          {dataUploaded && <SigmoidFilter setFilteredData={setFilteredData} />}
          <Button type="submit" sx={buttonStyle} variant="contained" disabled={loadingData}>
            {loadingData ? <CircularProgress size={20} /> : 'Upload Data'}
          </Button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </Box>
      </form>

      <Box sx={graphBox}>
        {dataUploaded ? (
          <>
            <KKTGraphs KKTGraph1={KKTGraph1} KKTGraph2={KKTGraph2} />
            <Button sx={buttonStyle} variant="contained" onClick={nextPage}>
              Continue
            </Button>
          </>
        ) : (
          <FileGuidelines />
        )}
      </Box>
    </Box>
  );
};

export default DataForm;
