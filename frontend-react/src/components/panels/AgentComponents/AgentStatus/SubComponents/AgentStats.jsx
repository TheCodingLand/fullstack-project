
import * as React from 'react';
// let defaultStyle = { 
//     color : '#fff' 
//   };
export default class AgentStats extends React.Component {
  render() {
    //console.log(this.props);
    return (this.props.user ?
      <div style={{ display: 'inline-block' }}><h3>{this.props.user.phoneLogin}</h3><h3>{this.props.user.prenom}</h3> </div> :
      <h3>loading Agent</h3>
    );
  }
}