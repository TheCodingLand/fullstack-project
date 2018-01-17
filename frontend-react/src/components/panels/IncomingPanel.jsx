
import * as React from 'react';
import Typography from 'material-ui/Typography';
import Stepper, { Step, StepLabel } from 'material-ui/Stepper';
import Grid from 'material-ui/Grid';
import { observer } from "mobx-react";

// let defaultStyle = { 
//     color : '#fff' 
//   };
function getSteps() {
    return ['inactive', 'client in line'];
  }

  let activestep= 2
@observer
export default class IncomingPanel extends React.Component {
   

    render () {
  
        function GetStepper(queue){
          console.log(queue.queue)
          activestep =0
          if (queue.queue.currentCall){

          if (queue.queue.currentCall.ucid){
            activestep = 1
          
          }}

      return (<Stepper activeStep = {activestep} alternativeLabel>
      {getSteps().map(label => {
        return (
          <Step key={label}>
            <StepLabel>{queue.queue.ext} : {label}</StepLabel>
          </Step>
        );
      })} 
    </Stepper>)

    }

      return(<div><Grid container spacing={24}>
        
        { this.props.queues && this.props.queues.map((queue) => { return (
          <Grid item xs>
         
          <GetStepper queue={queue} />
        </Grid>        
        )})}

        
        
      </Grid>
        </div>
      ); 
    }
  }
