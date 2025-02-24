import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import TOSImage from '../../images/TOS1.jpg';
import { useState} from 'react';
import ProjectSelector from './projectDialogs/ProjectSelector';

const commonStyles = {
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '15px',
  //padding: '15px',
  margin: '0',
  height: '85vh',
};

const image = {
  width: 'auto', // Adjust width as needed
  height: '300px', // Maintain aspect ratio
};

const TOS = ({handleLogin}) => {
  const [agreedToTOS, setAgreedToTOS] = useState(false);
  const handleCheckboxChange = (event) => {
    setAgreedToTOS(event.target.checked);
  };


  return (
    <Box sx={{padding:'15px'}}>
      <Box sx={commonStyles}>
        <Typography variant="body1" component="div">
          <Typography variant="h2" component="h2">Terms Of Service</Typography>
         
            The ISGP is an academic free software (freeware) subject to these Terms of Service. Some features of this software require an active Internet connection, necessary to access important documentation. We reserve the right to make changes to document names and content, descriptions or specifications of products or services, or other information without obligation to issue any notice of such changes. The website and any online content may periodically become unavailable due to maintenance or malfunction of computer equipment or other reasons.
            <br />
            You may view, download, and print Content that is available on this software and/or website, subject to the following conditions:
            <ol>
              <li>The Content may be used solely for internal informational purposes. No part of this software and/or website or its Content may be reproduced or transmitted in any form, by any means, electronic or mechanical, including photocopying and recording, for any other purpose. You may, however, use the option to make a movie of the program's progress.</li>
              <li>The Content may not be modified (well, if you have a good idea please let us know).</li>
              <li>Copyright and other proprietary notices may not be removed.</li>
              <li>You have no license or right to use the Content displayed on this software and/or website for other purposes than to analyze your data, except with our prior written permission.</li>
            </ol>
         
        </Typography>
        <img src={TOSImage} alt="Image" style={image} />
      </Box>
      <FormControlLabel control={<Checkbox onChange={handleCheckboxChange} color="success"/>} label="I Agree To The ISGP Terms of Service"/>
      {/* <Button disabled={!agreedToTOS} sx={{ textTransform: 'none', }} variant="contained" onClick={handleLogin}>Create Project</Button> */}
      <ProjectSelector agreedToTOS = {agreedToTOS}/>
      
    </Box>
  );
};

export default TOS;