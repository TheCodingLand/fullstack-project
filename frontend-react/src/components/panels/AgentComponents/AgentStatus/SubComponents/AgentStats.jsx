
import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import PhoneInTalk from '@material-ui/icons/PhoneInTalk';
import Phone from '@material-ui/icons/Phone';

import red from '@material-ui/core/colors/red';
import green from '@material-ui/core/colors/green';
import deepOrange from '@material-ui/core/colors/deepOrange';

import Divider from '@material-ui/core/Divider';
import AccountBox from '@material-ui/icons/AccountBox';
import { withTheme } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card'

import yellow from '@material-ui/core/colors/yellow';
import { observer } from "mobx-react";
import Tooltip from '@material-ui/core/Tooltip';
import cyan from '@material-ui/core/colors/cyan';

@observer
class AgentStats extends React.Component {

  render() {

    let user_icon = <AccountBox style={{ width: 25, height: 25, color: deepOrange[500] }} />

    if (this.props.user.phoneState === "ACDAVAIL") {
      user_icon = <Tooltip title="Available"><AccountBox style={{ width: 25, height: 25, color: green[500] }} /></Tooltip>
    }
    else if (this.props.user.phoneState === "Talking") {
      user_icon = <Tooltip title="Talking"><AccountBox style={{ width: 25, height: 25, color: cyan[500] }} /></Tooltip>
    }
    else if (this.props.user.phoneState === "Ringing") {
      
      user_icon = <Tooltip title="Ringing"><AccountBox style={{ width: 25, height: 25, color: yellow[500] }} /></Tooltip>
    }
    else if (this.props.user.phoneState === "Busy") {
      user_icon = <Tooltip title="Busy"><AccountBox style={{ width: 25, height: 25, color: yellow[500] }} /></Tooltip>
    }
    else {
      user_icon = <Tooltip title="Not Available"><AccountBox style={{ width: 25, height: 25, color: deepOrange[500] }} /></Tooltip>
    }


    let phone_icon;
    if (this.props.user.currentCall.ucid) {
      phone_icon = <PhoneInTalk style={{ color: green[500] }} />
      user_icon = <Tooltip title="Talking"><AccountBox style={{ width: 25, height: 25, color: cyan[500] }} /></Tooltip>
    }
    else {
      phone_icon = <Phone style={{ color: red[500] }} />;

    }


    return (this.props.user ?
      <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>

        {user_icon}

        <div> <Divider />
          <Typography>{this.props.user.ext}</Typography></div><Divider />{phone_icon}</Card></div> :
      <Typography>loading Agent</Typography>

    );
  }
}

export default withTheme()(AgentStats);