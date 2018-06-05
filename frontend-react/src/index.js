import React from 'react';
import ReactDOM from 'react-dom';
//import { green, purple, red } from '@material-ui/core/colors/green';
import green from '@material-ui/core/colors/green';
import purple from '@material-ui/core/colors/purple';
import red from '@material-ui/core/colors/red';
import 'typeface-roboto'
//MUI
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';



import App from './App';


const theme = createMuiTheme({
  typography: {
    fontWeightLight: 200,
 fontWeightRegular: 200,
 fontWeightMedium: 300},


  palette: {
    type: 'dark',
    primary: purple, // Purple and green play nicely together.
    secondary: {
      ...green,
      A400: '#00e677',
    },
    error: red,
  },
});



ReactDOM.render(<MuiThemeProvider theme={theme}><App /></MuiThemeProvider>, document.getElementById('root'));

