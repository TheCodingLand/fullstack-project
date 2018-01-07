
import * as React from 'react';
import { Grid, Cell } from 'styled-css-grid';
import AgentDetails from './SubComponents/AgentDetails';
import AgentStats from './SubComponents/AgentStats';
// let defaultStyle = { 
//     color : '#fff' 
//   };



export default class AgentItem extends React.Component {
  render() {
    //console.log(this.props);
    return (


      <Grid columns={2}>
        <AgentDetails user={this.props.user} />
        <AgentStats user={this.props.user} />
      </Grid>

    );
  }
}