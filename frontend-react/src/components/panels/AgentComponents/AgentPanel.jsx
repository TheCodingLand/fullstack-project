
import AgentItem from './AgentStatus/AgentItem';
import { Cell } from 'styled-css-grid';
import React from "react";

export default class AgentPanel extends React.Component {
 
    render () {
    return(
    <Cell  width={12}>
       <AgentItem user={this.props.user}/>
    </Cell>   
      ); 
    }
  };


