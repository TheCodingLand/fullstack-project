
import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card, { CardContent, CardMedia } from 'material-ui/Card';
import PhoneInTalk from 'material-ui-icons/PhoneInTalk';
import Phone from 'material-ui-icons/Phone';
import { red, green, deepOrange } from 'material-ui/colors';
import { withStyles } from 'material-ui/styles';
import Divider from 'material-ui/Divider/Divider';
import CardHeader from 'material-ui/Card/CardHeader';
import Avatar from 'material-ui/Avatar';
import AccountBox from 'material-ui-icons/AccountBox';
import { withTheme } from 'material-ui/styles';

import yellow from 'material-ui/colors/yellow';
import { observer } from "mobx-react";

@observer
class AgentStats extends React.Component {
    
    render () {
      let phone_icon = this.props.user.currentCall.ucid ? <PhoneInTalk style={{color: green[500]}} /> :<Phone style={{color: red[500]}}/> ;
      let user_icon = <AccountBox style={{ width: 25, height: 25, color: deepOrange[500]}} />

      if (this.props.user.phoneState === "ACDAVAIL")
      {
       user_icon = <AccountBox style={{ width: 25, height: 25, color: green[500]}} />
      } 
      else if (this.props.user.phoneState  == "Talking")
      {
        user_icon = <AccountBox style={{ width: 25, height: 25, color: green[500]}} />

      }
      else if (this.props.user.phoneState  == "Ringing")
      {
        phone_icon= <PhoneInTalk style={{color: yellow[500]}}/>
        user_icon = <AccountBox style={{ width: 25, height: 25, color: yellow[500]}} />
      }
      else if (this.props.user.phoneState  == "Busy")
      {
        user_icon = <AccountBox style={{ width: 25, height: 25, color: yellow[500]}} />
      }
      else
      {
        user_icon = <AccountBox style={{ width: 25, height: 25, color: deepOrange[500]}} />
      }
      const { theme } = this.props;
      const primaryText = theme.palette.text.primary;
      const primaryColor = theme.palette.primary[500];


      //let phonecolor = this.props.user.phoneState === "ACDAVAIL" ? red[500] : green[500];
      let phonecolor = this.props.user.currentCall ? red[500] : green[500];
      
      
      return(this.props.user ?
      <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
      {user_icon}

<div> <Divider />
      <Typography>{this.props.user.ext}</Typography></div><Divider />{phone_icon}</Card></div>  :
      <Typography>loading Agent</Typography>
      ); 
    }
  }

  export default withTheme()(AgentStats);