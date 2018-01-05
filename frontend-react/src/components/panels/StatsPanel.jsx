import * as React from 'react';
import logo from '../../logo.svg';
// let defaultStyle = { 
//     color : '#fff' 
//   };
export default class StatsPanel extends React.Component {
    render () {
      return(
        <div>
        <h3>Stats</h3>
         <img className="img-responsive" src={logo} alt="logo"/>
        </div>
      ); 
    }
  }