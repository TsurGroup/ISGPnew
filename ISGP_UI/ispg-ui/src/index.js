import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { ThemeProvider } from '@mui/material/styles';
import App from './App';
import theme from './theme/theme';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter} from 'react-router-dom'//export 'default not found without {}'

//import { ExperimentDataContext } from 'C:/Users/shema/CodingProjects/ISGP/ISGP_UI/ispg-ui/src/contexts/ExperimentDataContext.jsx';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
 
  <React.StrictMode>
     <BrowserRouter>
     <ThemeProvider theme={theme}>
     
    <App />
   
  </ThemeProvider>,
    </BrowserRouter>
  </React.StrictMode>
  
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
