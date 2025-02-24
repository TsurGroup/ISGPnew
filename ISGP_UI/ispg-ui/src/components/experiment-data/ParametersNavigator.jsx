import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';


export default function ParametersNavigator({ currentFormId,setCurrentFormId }) {

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation">
      <List>
        {['Algorithim Parameters', 'Population Parameters', 'Advanced Parameters'].map((text, index) => (
          <ListItem key={text} sx={{
            backgroundColor: index === currentFormId ? '#e0f7fa' : 'inherit', // Highlight selected item
          }} >
            <ListItemButton onClick={() => setCurrentFormId(index)}>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
    </Box>
  );

  return (
    <div>
    
        {DrawerList}
   
    </div>
  );
}
