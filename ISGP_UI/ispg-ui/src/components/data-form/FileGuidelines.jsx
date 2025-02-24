import React from 'react';
import { Box, Typography, Accordion, AccordionSummary, AccordionDetails, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';

import DataSetService from '../../services/DataSetService.js'


const FileGuidelines = () => {

  const downloadTextFile = async () => {
    try {
      
      const data = await DataSetService.getExampleTextFile();
      // Create a blob URL from the response
      const fileURL = window.URL.createObjectURL(new Blob([data]));
      
      // Create a link element to download the file
      const link = document.createElement('a');
      link.href = fileURL;
      link.setAttribute('download', 'downloaded_file.txt'); // Name for the downloaded file

      // Append the link to the document and simulate a click
      document.body.appendChild(link);
      link.click();

      // Clean up the link element
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading the file:', error);
    }
  };

  const downloadExcelFile = async () => {
    try {
      
      const data = await DataSetService.getExampleExcelFile();
      // Create a blob URL from the response
      const fileURL = window.URL.createObjectURL(new Blob([data]));
      
      // Create a link element to download the file
      const link = document.createElement('a');
      link.href = fileURL;
      link.setAttribute('download', 'example.xlsx');  // Set the file name

      // Append the link to the document and simulate a click
      document.body.appendChild(link);
      link.click();

      // Clean up the link element
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading the file:', error);
    }
  };

  return (
    <Box sx={{  maxWidth: '100%', wordWrap: 'break-word' }}>
      <Typography variant="h4" gutterBottom>
        Upload Your File
      </Typography>
      <Typography paragraph>
        To proceed, please upload either a text file or an Excel file that follows the required formats:
      </Typography>

      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel1a-content" id="panel1a-header">
          <Typography variant="h5">1. Text File Format (.txt):</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            <ul>
              <li>The text file should have <strong>3 columns</strong> separated by tabs.</li>
              <li>The columns should contain:
                <ul>
                  <li><strong>Column 1</strong>: Frequency values</li>
                  <li><strong>Column 2</strong>: Z' values (real impedance)</li>
                  <li><strong>Column 3</strong>: Z'' values (imaginary impedance)</li>
                </ul>
              </li>
              <li>No headers or extra formatting.</li>
            </ul>

            <Button  variant="contained" onClick={downloadTextFile}> Get </Button>
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="panel2a-content" id="panel2a-header">
          <Typography variant="h5">2. Excel File Format (.xlsx):</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            <ul>
              <li>The Excel file must have <strong>3 columns</strong>, and the <strong>first row</strong> should contain the headers:</li>
              <ul>
                <li><strong>Column 1</strong>: "Freq" (Frequency)</li>
                <li><strong>Column 2</strong>: "Z' (a)" (Real Impedance)</li>
                <li><strong>Column 3</strong>: "Z'' (b)" (Imaginary Impedance)</li>
              </ul>
            </ul>

             <Button  variant="contained" onClick={downloadExcelFile}> Get </Button>
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Typography variant="body1" sx={{ marginTop: '10px' }}>
        <strong>Please ensure your file follows the correct format to avoid errors.</strong>
      </Typography>
    </Box>
  );
};

export default FileGuidelines;
