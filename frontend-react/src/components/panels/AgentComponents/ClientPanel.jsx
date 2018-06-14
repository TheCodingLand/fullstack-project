
import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import Divider from '@material-ui/core/Divider';
import { observer } from "mobx-react";
import Pbar from './ProgressBar/ProgressBar'


@observer
class ClientPanel extends React.Component {
    
    render () {
      let possibleClients = []
      if (this.props.user.currentCall.possibleClients){
        console.log(this.props.user.currentCall.possibleClients)
        
        if (this.props.user.currentCall.possibleClients.length > 0) {
          console.log("FOUND CLIENT" + this.props.user.currentCall.possibleClients )
        possibleClients = this.props.user.currentCall.possibleClients.slice(0,1).map((client) => {return <Typography key={client.otId}>{client.Lastname} {client.FirstName}</Typography>}) }
      }
      

        return(this.props.user.currentCall.ucid ?
       <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <div><Typography>{this.props.user.currentCall.origin}</Typography>{possibleClients}</div><Divider />
        
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