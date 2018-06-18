
import React from 'react';
import Drawer from '@material-ui/core/Drawer';
import TicketForm from './TicketForm';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';

import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';

import Select from '@material-ui/core/Select';
import { observer } from "mobx-react";

const styles = {
  list: {
    width: 250,
  },
  listFull: {
    width: 'auto',
  },
};

@observer
class TicketDrawer extends React.Component {
  
state ={
  open : false,
  agent: false
}
handleChange = event => {
  this.setState({ [event.target.name]: event.target.value });
  this.props.store.agentStore.agents.forEach(agent => { if (agent === event.target.value) { 
    this.props.store.agentStore.setCurrentUser(agent); 
   }
  });
};

handleDrawerOpen = () => {
  this.setState({ open: true });
};


handleDrawerClose = () => {
  this.setState({ open: false });
};



render() {
  
  const { classes } = this.props;

 return (
  
    <div>
      
 {this.state.agent ? <Button color="secondary" onClick={ () => {this.handleDrawerOpen();}}>Open Ticket ({this.state.agent.callsWithoutTickets.length})</Button> :
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="age-helper">My Extention</InputLabel>
          <Select
            onChange={this.handleChange}
            input={<Input value="default" name="agent" id="age-helper" />}
          >
          { this.props.store.agentStore.agents.map((agent) => {
          return <MenuItem key={agent.ext} value={agent}>{agent.ext}</MenuItem> } )}
          
          </Select>
        </FormControl>}
 <Drawer
 anchor="bottom"
 open={this.state.open}
 onClose={ () => {this.handleDrawerClose();}}>
  <div>
          <div>
          
            <IconButton onClick={() => {this.handleDrawerClose()}}>
            <ExpandMoreIcon />
            </IconButton> 
          </div>
 
   <div><TicketForm store={this.props.store} categories={this.props.categories} agent={this.state.agent} /></div>
 </div>
</Drawer>
</div>
)}
}

export default withStyles(styles)(TicketDrawer);