import React from 'react';
import { Paper } from '@mui/material';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';


const PaperContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  //gap:'30px',
  //width:'30%',
  height: '10px'
}));

const commonStyles = {
  padding: '10px',
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  //justifyContent: 'space-between',
  gap:'10px',
  //width:'30%',
  height: '10px'
};

const Label = styled('label')(({ theme }) => ({
  ...theme.typography.body1,
  color: theme.palette.text.primary,
  fontWeight: 'bold',
  minWidth: '50px'
}));

const Value = styled('div')(({ theme }) => ({
  ...theme.typography.body1,
  color: theme.palette.text.secondary,
}));

const DataItem = ({ label, value }) => {
  return (
    <Box style={commonStyles}>
    {/* // <PaperContainer elevation={3}> */}
      <Label>{label+':'}</Label>
      <Value>{value}</Value>
      </Box>
    // </PaperContainer>
  );
};

export default DataItem;