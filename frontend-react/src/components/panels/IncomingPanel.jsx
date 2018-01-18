
import * as React from 'react';
import Typography from 'material-ui/Typography';
import Stepper, { Step, StepLabel } from 'material-ui/Stepper';
import Grid from 'material-ui/Grid';
import { observer } from "mobx-react";

let activestep= 2
  
@observer
export default class IncomingPanel extends React.Component {
   

    render () {
  
        function GetStepper(queue){
          console.log(queue.queue)
          let steps = []
          activestep =-1
          if (queue.queue.currentCall){

          if (queue.queue.currentCall.ucid){
            activestep = 0
            steps.push(<Step><StepLabel>Contact Phone : {queue.queue.currentCall.origin}</StepLabel></Step>)

          if (queue.queue.currentCall.callType) {
            activestep = 1
            steps.push(<Step><StepLabel>Waiting Line : {queue.queue.currentCall.callType}</StepLabel></Step>)
          }

          else
          {
            steps.push(<Step><StepLabel>Client in menus</StepLabel></Step>)
          }
          }
          else{
            steps.push(<Step><StepLabel>No Calls</StepLabel></Step>)
            steps.push(<Step><StepLabel>Free</StepLabel></Step>)
          }
        }

      return (<Stepper activeStep = {activestep} alternativeLabel>{steps}</Stepper>)
    }

      return(<div><Grid container spacing={24}>
        
        { this.props.queues && this.props.queues.map((queue) => { return (
          <Grid item xs>
          <GetStepper queue={queue} />
        </Grid>)})}
      </Grid>
        </div>
      ); 
    }
  }
