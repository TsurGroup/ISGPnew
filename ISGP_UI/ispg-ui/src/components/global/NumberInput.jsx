import React from 'react';
import Box from '@mui/material/Box';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import { styled } from '@mui/material/styles';
import { useForm } from '../../contexts/FormContext';

const NumberInput = ({ name, index, minValue, maxValue, increment, size = "big", disabled = false }) => {
  const { formData, handleChange, handleDictChange } = useForm();
  
  const roundTo = (num) => Math.round(num * 100) / 100;

  const handleIncrement = () => {
    if (disabled) return;
    const currentValue = (index !== undefined && index !== null) ? formData[name]?.[index] : formData[name] || minValue;
    const incrementedValue = roundTo(Math.min(currentValue + increment, maxValue));
    if (index !== undefined && index !== null) {
      console.log(index);
      handleDictChange(name, index, incrementedValue);
    } else {
      console.log({ name, value: incrementedValue });
      handleChange({ target: { name, value: incrementedValue } });
    }
  };

  const handleDecrement = () => {
    if (disabled) return;
    const currentValue = (index !== undefined && index !== null) ? formData[name]?.[index] : formData[name] || minValue;
    const decrementedValue = roundTo(Math.max(currentValue - increment, minValue));
    if (index !== undefined && index !== null) {
      console.log(index);
      handleDictChange(name, index, decrementedValue);
    } else {
      handleChange({ target: { name, value: decrementedValue } });
    }
  };

  const handleInputChange = (event) => {
    if (disabled) return;
    const newValue = Number(parseFloat(event.target.value));
    if (newValue >= minValue && newValue <= maxValue) {
      if (index !== undefined && index !== null) {
        handleDictChange(name, index, newValue);
      } else {
        handleChange(event);
      }
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <StyledButton type="button" onClick={handleDecrement} size={size} disabled={disabled} aria-label="Decrement">
        <RemoveIcon />
      </StyledButton>
      <StyledInput 
        type="number" 
        name={name} 
        value={(index !== undefined && index !== null) ? formData[name]?.[index] : formData[name] || minValue} 
        onChange={handleInputChange} 
        size={size} 
        disabled={disabled} 
        aria-label={name} 
      />
      <StyledButton type="button" onClick={handleIncrement} size={size} disabled={disabled} aria-label="Increment">
        <AddIcon />
      </StyledButton>
    </Box>
  );
};

const blue = {
  100: '#daecff',
  200: '#b6daff',
  300: '#66b2ff',
  400: '#3399ff',
  500: '#007fff',
  600: '#0072e5',
  700: '#0059B2',
  800: '#004c99',
};

const grey = {
  50: '#F3F6F9',
  100: '#E5EAF2',
  200: '#DAE2ED',
  300: '#C7D0DD',
  400: '#B0B8C4',
  500: '#9DA8B7',
  600: '#6B7A90',
  700: '#434D5B',
  800: '#303740',
  900: '#1C2025',
};

// Adjust the styles based on the `size` and `disabled` props
const StyledInput = styled('input')(({ theme, size, disabled }) => ({
  fontSize: size === 'small' ? '0.75rem' : '1rem',
  padding: size === 'small' ? '4px 6px' : '10px 12px',
  width: size === 'small' ? '1.5rem' : '4rem',
  fontFamily: 'inherit',
  fontWeight: 400,
  lineHeight: 1.375,
  color: grey[900],
  background: disabled ? grey[200] : '#fff',
  border: `1px solid ${disabled ? grey[300] : grey[200]}`,
  boxShadow: disabled ? 'none' : `0px 2px 4px rgba(0,0,0,0.05)`,
  borderRadius: '8px',
  margin: '0 8px',
  outline: 0,
  textAlign: 'center',
  transition: 'border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out',

  '&:hover': {
    borderColor: !disabled && blue[400],
  },

  '&:focus': {
    borderColor: !disabled && blue[400],
    boxShadow: !disabled && `0 0 0 3px ${blue[200]}`,
  },

  '&:focus-visible': {
    outline: 0,
  },

  '&::-webkit-outer-spin-button, &::-webkit-inner-spin-button': {
    '-webkit-appearance': 'none',
    margin: 0,
  },

  '&[type=number]': {
    '-moz-appearance': 'textfield',
  },
}));

const StyledButton = styled('button')(({ theme, size, disabled }) => ({
  width: size === 'small' ? '24px' : '32px',
  height: size === 'small' ? '24px' : '32px',
  fontFamily: 'IBM Plex Sans, sans-serif',
  fontSize: size === 'small' ? '0.75rem' : '0.875rem',
  boxSizing: 'border-box',
  lineHeight: 1.5,
  border: '1px solid',
  borderRadius: '999px',
  borderColor: disabled ? grey[300] : grey[200],
  background: disabled ? grey[100] : grey[50],
  color: disabled ? grey[500] : grey[900],
  display: 'flex',
  flexFlow: 'row nowrap',
  justifyContent: 'center',
  alignItems: 'center',
  transitionProperty: 'all',
  transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)',
  transitionDuration: '120ms',
  cursor: disabled ? 'not-allowed' : 'pointer',

  '&:hover': {
    background: !disabled && blue[500],
    borderColor: !disabled && blue[400],
    color: !disabled && grey[50],
  },

  '&:focus-visible': {
    outline: 0,
  },
}));

export default NumberInput;
