import React, { Component } from "react";
import { observer } from "mobx-react";

const Agent = observer(({ agent }) => (
  <li>{agent.firstname}{agent.phoneLogin}{agent.ext}{agent.phoneState}
    
  </li>
));

export default Agent;