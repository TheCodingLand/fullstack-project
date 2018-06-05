
import * as React from 'react';
//import { Grid, Cell } from 'styled-css-grid';
import AgentDetails from './SubComponents/AgentDetails';
import AgentStats from './SubComponents/AgentStats';
// let defaultStyle = { 
//     color : '#fff' 
//   };

import GridMaterial from '@material-ui/core/Grid';

export default class AgentItem extends React.Component {
  render() {
    return (
      <GridMaterial container style={{ flexGrow: 1 }}>
        <GridMaterial item xs={12}>
          <GridMaterial container direction='row' justify='flex-start' >
            <GridMaterial item style={{ flex: 'auto', height: "100px", width: "75%", paddingRight: "0px"  }}>
              <AgentDetails user={this.props.user} />
            </GridMaterial>
            <GridMaterial item style={{ flex: 'auto', height: "100px", width: "25%" }}>
              <AgentStats user={this.props.user} />
            </GridMaterial>
          </GridMaterial>
        </GridMaterial>
      </GridMaterial>
    );
  }
}

