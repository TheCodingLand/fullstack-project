import Spinner from 'react-spinner-material';
import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';

export default class Loader extends Component {
  render() {
  return (
      <div>
          <Typography>
            Loading...
          </Typography>
       <Spinner
     
        size={500}
        spinnerColor={"#FFFFFF"}
        spinnerWidth={2}
        visible={true} />
      </div>
    );
  }
}