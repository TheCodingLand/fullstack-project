
import * as React from 'react';
import Typography from 'material-ui/Typography';
import Stepper, { Step, StepLabel } from 'material-ui/Stepper';
import Grid from 'material-ui/Grid';
import { observer } from "mobx-react";
import { queue } from 'async';
// let defaultStyle = { 
//     color : '#fff' 
//   };
function getSteps() {
    return ['inactive', 'client in line'];
  }
@observer
export default class IncomingPanel extends React.Component {
    

    render () {
    
    const steps = getSteps();
    let activestep=0
    if (this.props.queues.currentCall){
    if(this.props.queues.currentCall.ucid){
      activestep= 1
    }
    }

      return(
        <div><Grid container spacing={24}>
        
        { this.props.queues && this.props.queues.map((queue) => { return (
          <Grid item xs>
          {console.log(queue)}
          
          <Stepper activestep = {activestep} alternativeLabel>
          {steps.map(label => {
            return (
              <Step key={label}>
                <StepLabel>{queue.ext} : {label}</StepLabel>
              </Step>
            );
          })} 
        </Stepper>
        </Grid>        
        )})}

        
        
      </Grid>
        </div>
      ); 
    }
  }
