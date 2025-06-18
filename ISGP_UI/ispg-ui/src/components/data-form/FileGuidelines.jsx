import React, { useState } from 'react';
import { 
  Box, Typography, Accordion, AccordionSummary, 
  AccordionDetails, Button, CircularProgress 
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DataSetService from '../../services/DataSetService';

const FileGuidelines = () => {
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState({ text: false, excel: false });

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    if (!loading.text && !loading.excel) {  // Prevent opening if downloading
      setExpanded(isExpanded ? panel : false);
    }
  };

  const downloadFile = async (type) => {
    setLoading((prev) => ({ ...prev, [type]: true })); // Show spinner & disable button

    try {
      if (type === 'text') {
        await DataSetService.getExampleTextFile();
      } else {
        await DataSetService.getExampleExcelFile();
      }
    } catch (error) {
      console.error(`Error downloading ${type} file:`, error);
    } finally {
      setLoading((prev) => ({ ...prev, [type]: false })); // Hide spinner & enable button
    }
  };

  return (
    <Box sx={{ maxWidth: '100%', wordWrap: 'break-word' }}>
      <Typography variant="h4" gutterBottom>
        Upload Your File
      </Typography>
      <Typography paragraph>
        To proceed, please upload either a text file or an Excel file that follows the required formats:
      </Typography>

      {/* Text File Accordion */}
      <Accordion 
        expanded={expanded === 'text'} 
        onChange={handleAccordionChange('text')}
        disabled={loading.text || loading.excel}  // Disable accordion while downloading
      >
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
            <Button 
              variant="contained" 
              onClick={() => downloadFile('text')}
              disabled={loading.text || loading.excel}  // Disable button while downloading
              sx={{ display: 'flex', alignItems: 'center', gap: 1, textTransform: 'none' }}
            >
              {loading.text ? <CircularProgress size={20} /> : 'Download Example'}
            </Button>
          </Typography>
        </AccordionDetails>
      </Accordion>

      {/* Excel File Accordion */}
      <Accordion 
        expanded={expanded === 'excel'} 
        onChange={handleAccordionChange('excel')}
        disabled={loading.text || loading.excel}  // Disable accordion while downloading
      >
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
            <Button 
              variant="contained" 
              onClick={() => downloadFile('excel')}
              disabled={loading.text || loading.excel}  // Disable button while downloading
              sx={{ display: 'flex', alignItems: 'center', gap: 1,textTransform: 'none'}}
            >
              {loading.excel ? <CircularProgress size={20} /> : 'Download Example'}
            </Button>
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
