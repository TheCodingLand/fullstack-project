
import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import Divider from '@material-ui/core/Divider';
import { observer } from "mobx-react";
import Tooltip from '@material-ui/core/Tooltip';
import { withStyles } from '@material-ui/core/styles';

import purple from '@material-ui/core/colors/purple';
// const styles = {
//   root: {
//     background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
//     borderRadius: 3,
//     border: 0,
//     color: 'white',
//     height: 48,
//     padding: '0 30px',
//     boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .30)',
//   },
//   label: {
//     textTransform: 'capitalize',
//   },
// };

const style={

  color: purple[500],

}

const styles = theme => ({

  tooltip: {
    color: purple[500],
    
  },
});

@observer
class ClientPanel extends React.Component {
  
    render () {
      
      const { classes } = this.props;
      let possibleClients = []
      if (this.props.user.currentCall.possibleClients){
        console.log(this.props.user.currentCall.possibleClients)
        
        if (this.props.user.currentCall.possibleClients.length > 0) {
          console.log("FOUND CLIENT" + this.props.user.currentCall.possibleClients )
        possibleClients = this.props.user.currentCall.possibleClients.slice(0,1).map((client) => {return <Typography key={client.otId}>{client.Lastname} {client.FirstName}</Typography>}) }
      }
      

        return(this.props.user.currentCall.ucid ?
       <div><Tooltip style={style} className={classes.Tooltip} title={this.props.user.currentCall.origin + "->" + this.props.user.currentCall.destination}>
         <Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <div><Typography color="secondary">{this.props.user.currentCall.origin}</Typography>{possibleClients}</div><Divider />
        
        <div><Typography color="secondary">{this.props.user.currentCall.callType}</Typography></div>
      
        
          
          </Card></Tooltip></div>
          :
          <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <Typography>No Calls in progress</Typography>
        </Card></div>
        ); 
      }
    }

  
    export default withStyles(styles)(ClientPanel);
    