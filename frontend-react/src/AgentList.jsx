import React, { Component } from "react";
//import { observable, action } from "mobx";
import { observer } from "mobx-react";

import Agent from "./Agent";

@observer
export default class AgentList extends React.Component {
  

  render() {
    return (
      <div>       
        <hr />
        <ul>
          {this.props.store.agents.map(agent => (
            <Agent agent={agent} key={agent.phoneLogin} />
          ))}
        </ul>
      </div>
    );
  }
}
