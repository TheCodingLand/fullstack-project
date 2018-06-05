
import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import Divider from '@material-ui/core/Divider';
import { observer } from "mobx-react";
import Pbar from './ProgressBar/ProgressBar'


@observer
class ClientPanel extends React.Component {


    render () {
        return(this.props.user.currentCall.ucid ?
       <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <div><Typography>{this.props.user.currentCall.origin}</Typography></div><Divider />
        
        <div><Typography>{this.props.user.currentCall.callType}</Typography></div>
      
        <Pbar starttime={this.props.user.currentCall.starttime} />
          
          </Card></div>
          :
          <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <Typography>No Calls in progress</Typography>
        </Card></div>
        ); 
      }
    }

  export default ClientPanel;