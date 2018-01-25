
import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card from 'material-ui/Card';
import Divider from 'material-ui/Divider/Divider';
import { withTheme } from 'material-ui/styles';
import { withStyles } from 'material-ui/styles';
import { observer } from "mobx-react";
import ProgressBar from './ProgressBar/ProgressBar'
import { Tooltip } from 'material-ui/Tooltip';
// let defaultStyle = { 
//     color : '#fff' 
//   };

@observer
class ClientPanel extends React.Component {


    render () {
        return(this.props.user.currentCall.ucid ?
       <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <div><Typography>{this.props.user.currentCall.origin}</Typography></div><Divider />
        
        <div><Typography>{this.props.user.currentCall.callType}</Typography></div>
      
          <ProgressBar starttime={this.props.user.currentCall.starttime} />
          
          </Card></div>
          :
          <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <Typography>No Calls in progress</Typography>
        </Card></div>
        ); 
      }
    }



    
    

  export default withTheme()(ClientPanel);