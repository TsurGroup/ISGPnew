import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#308fac', // New primary color#308fac
    },
    secondary: {
      main: '#0457ac', // New secondary color
    },

    third: {
      main: '#a7e237', // New secondary color
    },
    success: {
      main: '#37bd79', // Success color
    },
    warning: {
      main: '#f4e604', // Warning color
    },
    error: {
      main: '#f4e604', // Error color
    },
    background: {
      default: '#f4f6f8', // Default background color
      paper: '#ffffff', // Background color for Paper components
    },
    text: {
      primary: '#308fac', // Updated to align with new primary color
      secondary: '#555555', // Secondary text color remains
    },
  },
  typography: {
    fontFamily: '"Montserrat", "Roboto", "Helvetica", "Arial", sans-serif', // Retain Montserrat
    h1: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '1.75rem',
      fontWeight: 'bold',
    },
    h3: {
      fontSize: '1.25rem',
      fontWeight: 'bold',
    },
    body1: {
      fontSize: '1rem', // Fix spacing issue in font size
      fontWeight: 500,
      color: '#555555',
    },
    body2: {
      fontSize: '0.8rem',
      color: '#555555',
    },
  },
  spacing: 8, // Default spacing unit
});

export default theme;
