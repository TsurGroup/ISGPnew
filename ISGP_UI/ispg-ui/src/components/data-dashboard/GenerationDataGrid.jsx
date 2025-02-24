import DataItem from '../global/DataItem';
import Box from '@mui/material/Box';

const commonStyles = {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '15px',
    position: 'relative',
    width: '50%',
    //padding:'10px'
};

const GenerationDataGrid = ({props}) => {
    return (
        <Box sx={commonStyles}>
            <DataItem label={'Run Number'} value={props.run} />
            <DataItem label={'Compatibility'} value={props.fitness} />
            <DataItem label={'Generation Number'} value={props.generation} />
            <DataItem label={'Area'} value={props.area} />
        </Box>
    );
};

export default GenerationDataGrid;