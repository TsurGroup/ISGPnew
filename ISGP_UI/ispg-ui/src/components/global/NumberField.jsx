import NumberInput from './NumberInput';
import Box from '@mui/material/Box';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import Tooltip from '@mui/material/Tooltip';




const commonStyles = {
    padding: '10px',
    display:'flex',
    flexDirection:'row',
    alignItems: 'center',
    //border: '1px solid black',
    //justifyContent: 'center',
    gap:'30px',
    borderRadius: '10px',
    //margin: 'auto',
    
  };


const NumberField = ({ name, defaultValue, minValue, maxValue, increment, label,disabled,toolTip }) => {
    return(
        <Box style = {commonStyles}>
              <Tooltip title={toolTip}>
              <InfoOutlinedIcon />
             </Tooltip>
            {label ? <label style={ {minWidth: '200px'}}> {label}: </label> : null} 
        <NumberInput  name={name} minValue={minValue} maxValue={maxValue} increment={increment} defaultValue={defaultValue} disabled={disabled}/>
        </Box>
    ) 
  }

  export default NumberField;

  //was min 200px b4 change