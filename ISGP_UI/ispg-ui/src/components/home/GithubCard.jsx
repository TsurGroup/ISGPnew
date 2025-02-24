import React from 'react'
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import CardMedia from '@mui/material/CardMedia';
import backgroundImage from '../../images/github1.png';

const GithubCard = () => {
    return (
        <Card sx={{ minWidth: 250 }}>
         <CardMedia
        sx={{ height: 275 }}
        image={backgroundImage}
        title="green iguana"
      />
          <CardContent>
            abcd
          </CardContent>
          <CardActions>
            {/* <Button size="small">Learn More</Button> */}
          </CardActions>
        </Card>
    )
}

export default GithubCard
