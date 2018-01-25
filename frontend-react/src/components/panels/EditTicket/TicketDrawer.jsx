
import React from 'react';
import Drawer from 'material-ui/Drawer';
import TicketForm from './TicketForm';
import Button from 'material-ui/Button';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import { withStyles } from 'material-ui/styles';

const styles = {
  list: {
    width: 250,
  },
  listFull: {
    width: 'auto',
  },
};


class TicketDrawer extends React.Component {
  
state ={
  open : false
}

handleDrawerOpen = () => {
  this.setState({ open: true });
};


handleDrawerClose = () => {
  this.setState({ open: false });
};

render() {
  const { open } = this.state;  
 return (
  
    <div>
        <Button onClick={ () => {this.handleDrawerOpen();}}>Open Ticket</Button>
 <Drawer
 anchor="bottom"
 open={this.state.open}
 onClose={ () => {this.handleDrawerClose();}}>
  <div>
          <div>
            <IconButton onClick={() => {this.handleDrawerClose();}}>
            <ExpandMoreIcon />
            </IconButton>
          </div>
 
   <div><TicketForm /></div>
 </div>
</Drawer>
</div>
)}
}

export default withStyles(styles)(TicketDrawer);