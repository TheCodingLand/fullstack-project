
import AgentItem from './AgentStatus/AgentItem';
import { Grid, Cell } from 'styled-css-grid';
import React from "react";

export default class AgentPanel extends React.Component {
 
  
    render () {
    
    console.log(this.props);
   
    return(
    <Cell width={12}>
     
       <AgentItem user={this.props.user}/>
   
    </Cell>   
      ); 
    }
  };


