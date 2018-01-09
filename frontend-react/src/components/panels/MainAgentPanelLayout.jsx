import * as React from 'react';
import { Grid, Cell } from 'styled-css-grid';
import AgentPanel from './AgentComponents/AgentPanel';
import ClientPanel from './AgentComponents/ClientPanel';
import TicketsPanel from './AgentComponents/TicketsPanel';

// let defaultStyle = { 
//     color : '#fff' 
//   };
export default class MainAgentPanel extends React.Component {
    render () {
      return(
        <Grid alignContent="stretch" minRowHeight="100px" columns = {3}>
        <Cell width={1} height={1}><AgentPanel user={this.props.user} /></Cell>
        <Cell width={1} height={1}><ClientPanel user={this.props.user} /></Cell>
        <Cell width={1} height={1}><TicketsPanel user={this.props.user} /></Cell>
        </Grid>
      ); 
    }
  }