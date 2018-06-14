
import React from 'react';
import Select from '@material-ui/core/Select';
import TextField from '@material-ui/core/TextField';
import { observer } from "mobx-react";
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';

import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({

  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  selects: {
    marginLeft: theme.spacing.unit,
  },
  textFieldSmall: {

    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: '29%',
  },
})






@observer
class ClientForm extends React.Component {
  state = {
    otId: "",
    FirstName: "",
    LastName: "",
  

  }

  handleChange = name => event => {

    this.setState({
      [name]: event.target.value,
    });
    
    if (name === "FirstName") {
    
      this.props.onClientSelect({
        otId:"",
        FirstName:event.target.value,
        LastName:this.state.LastName
      })
    }
    if (name === "LastName") {
    
      this.props.onClientSelect({
        otId:"",
        LastName:event.target.value,
        FirstName:this.state.FirstName
      })
    }
  
    
  
}


  

  handleClientChange = name => event => {

    this.setState({
      [name]: event.target.value,
    });
    
   
    this.props.possibleClients.forEach((c) => {
      if (c) {
        if (c.otId === event.target.value) {
          console.log(c.otId)
          this.setState({ otId: c.otId, FirstName: c.FirstName, LastName: c.LastName })
          console.log(c)
          this.props.onClientSelect(c)
        }
      }
    })
    
  
  };


  render() {
   
    let menuitems = []
    if (this.props.possibleClients.length > 0) {

      menuitems = this.props.possibleClients.map((client) => { return <MenuItem key={client.otId} value={client.otId}>{client.FirstName} {client.LastName}</MenuItem> })
    }
    else {
      menuitems = [<MenuItem key={1} origin="nothing" value="None">None</MenuItem>,]
    }
    const { classes } = this.props;
    return (<div>
      <FormControl fullWidth={true} className={classes.selects}>
        <InputLabel htmlFor="otId">Client</InputLabel>

        <Select className={classes.selects}
          required
          value={this.state.otId}
          onChange={this.handleClientChange('otId')}
        >
          {menuitems}
        </Select>
        </FormControl>
        <FormHelperText>Select Client</FormHelperText>

        <TextField
          required
         
          id="Firstname"
          label="First name"
          className={classes.textFieldSmall}
          margin="normal"
          onChange={this.handleChange('FirstName')}
          value={this.state.FirstName}
        />
        <TextField
          required
          
          id="Lastname"
          label="Last name"
          className={classes.textFieldSmall}
          margin="normal"
          on
          onChange={this.handleChange('LastName')}
          value={this.state.LastName}
        /></div>
      )
  }
}

export default withStyles(styles)(ClientForm);