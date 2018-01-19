
import * as React from 'react';
//import { Grid, Cell } from 'styled-css-grid';
import AgentDetails from './SubComponents/AgentDetails';
import AgentStats from './SubComponents/AgentStats';
// let defaultStyle = { 
//     color : '#fff' 
//   };

import Grid from 'material-ui/Grid';

export default class AgentItem extends React.Component {
  render() {
    return (
      <Grid container style={{ flexGrow: 1 }}>
        <Grid item xs={12}>
          <Grid container direction='row' justify='flex-start' >
            <Grid item style={{ flex: 'auto', height: "100px", width: "75%", paddingRight: "0px"  }}>
              <AgentDetails user={this.props.user} />
            </Grid>
            <Grid item style={{ flex: 'auto', height: "100px", width: "25%" }}>
              <AgentStats user={this.props.user} />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

