import React, { useState, useEffect } from 'react';
import { Divider, Grid, Checkbox, Typography, Box, BottomNavigation, BottomNavigationAction } from '@mui/material';
import NumberInput from '../global/NumberInput';
import NumberField from '../global/NumberField';
import { useForm } from '../../contexts/FormContext';

const commonStyles = {
  padding: '20px',
  display: 'flex',
  flexDirection: 'column',
  border: '1px solid black',
  borderRadius: '10px',
  margin: '0',
  justifyContent: 'center',
  gap: '10px',
  width: '100%'
};

// Define category mapping
const CATEGORIES = [
  { label: "Population", key: "General" },
  { label: "Out Of Bounds Peak", key: "OutOfBounds" },
  { label: "Negative Peak", key: "Negative" },
  { label: "Forced Peak", key: "Forced", disabled: true }
];

const PopulationParameters = () => {
  const { formData, handleListChange } = useForm();
  const [tab, setTab] = useState(0);  // Active tab index
  const [filteredItems, setFilteredItems] = useState([]);  // Filtered function list

  useEffect(() => {
    if (formData?.functionTypes) {
      // Get the selected category from CATEGORIES
      const selectedCategory = CATEGORIES[tab].key;
      
      // Filter items based on category
      const newItems = formData.functionTypes.filter(ft => ft.category === selectedCategory);
      setFilteredItems(newItems);
    }
  }, [formData, tab]);

  const handleCheckboxChange = (type, value) => {
    // Update the list of selected items by Enum value
    handleListChange(type, value);
  };

  return (
    <Box component="fieldset" style={commonStyles}>
      <legend>Population Parameters</legend>
      <NumberField
        name="populationSize"
        defaultValue={20}
        minValue={10}
        maxValue={30}
        increment={1}
        label={'Population size'}
      />
      <Divider />
      
      <Box style={{ maxHeight: '300px', minHeight: '250px', overflow: 'auto', marginTop: '10px' }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={2} />
          <Grid item xs={2}>
            <Typography align="center">initial:</Typography>
          </Grid>
          <Grid item xs={2}>
            <Typography align="center">mutation:</Typography>
          </Grid>
          <Grid item xs={3}>
            <Typography align="center">lb:</Typography>
          </Grid>
          <Grid item xs={3}>
            <Typography align="center">ul:</Typography>
          </Grid>

          {filteredItems.map((item, index) => (
            <React.Fragment key={item.value}>
              <Grid item xs={3}>
                <Typography align="center" variant="caption">{item.description}</Typography>
              </Grid>
              <Grid item xs={1.5} container justifyContent="center">
                <Checkbox
                  checked={formData['initialFunctions']?.includes(item.value)}  // Use item.value (Enum value)
                  onChange={() => handleCheckboxChange('initialFunctions', item.value)}  // Pass item.value
                />
              </Grid>
              <Grid item xs={1.5} container justifyContent="center">
                <Checkbox
                  checked={formData['mutationFunctions']?.includes(item.value)}  // Use item.value (Enum value)
                  onChange={() => handleCheckboxChange('mutationFunctions', item.value)}  // Pass item.value
                />
              </Grid>
              <Grid item xs={3} container justifyContent="flex-end">
                <NumberInput name="lowerBounds" index={item.value} minValue={-100} maxValue={500} increment={0.1} size="small" />
              </Grid>
              <Grid item xs={3} container justifyContent="flex-end" sx={{ paddingRight: '10px' }}>
                <NumberInput name="upperBounds" index={item.value} minValue={-100} maxValue={500} increment={0.1} size="small" />
              </Grid>
            </React.Fragment>
          ))}
        </Grid>
      </Box>

      {/* Bottom Navigation */}
      <BottomNavigation
        value={tab}
        onChange={(event, newValue) => setTab(newValue)}
        showLabels
        sx={{ marginTop: '10px', borderTop: '1px solid #ccc' }}
      >
        {CATEGORIES.map((category, index) => (
          <BottomNavigationAction
            key={category.key}
            label={category.label}
            disabled={category.disabled}
          />
        ))}
      </BottomNavigation>
    </Box>
  );
};

export default PopulationParameters;
