
import * as React from 'react';
import Typography from 'material-ui/Typography';
import PhoneInTalk from 'material-ui-icons/PhoneInTalk';
import Phone from 'material-ui-icons/Phone';
import { red, green, deepOrange } from 'material-ui/colors';
import Divider from 'material-ui/Divider/Divider';
import AccountBox from 'material-ui-icons/AccountBox';
import { withTheme } from 'material-ui/styles';
import Card from 'material-ui/Card'
import yellow from 'material-ui/colors/yellow';
import { observer } from "mobx-react";
import Tooltip from 'material-ui/Tooltip';
import cyan from 'material-ui/colors/cyan';
@observer
class AgentStats extends React.Component {
    
    render () {
      //let phone_icon = this.props.user.currentCall.ucid ? <PhoneInTalk style={{color: green[500]}} /> :<Phone style={{color: red[500]}}/> ;
      let user_icon = <AccountBox style={{ width: 25, height: 25, color: deepOrange[500]}} />

      if (this.props.user.phoneState === "ACDAVAIL")
      {
       user_icon = <Tooltip title="Available"><AccountBox style={{ width: 25, height: 25, color: green[500]}} /></Tooltip>
      } 
      else if (this.props.user.phoneState  === "Talking")
      {
        user_icon = <Tooltip title="Talking"><AccountBox style={{ width: 25, height: 25, color: cyan[500]}} /></Tooltip>

      }
      else if (this.props.user.phoneState  === "Ringing")
      {
        phone_icon= <PhoneInTalk style={{color: yellow[500]}}/>
        user_icon = <AccountBox style={{ width: 25, height: 25, color: yellow[500]}} />
      }
      else if (this.props.user.phoneState  === "Busy")
      {
        user_icon = <Tooltip title="Busy"><AccountBox style={{ width: 25, height: 25, color: yellow[500]}} /></Tooltip>
      }
      else
      {
        user_icon = <Tooltip title="Not Available"><AccountBox style={{ width: 25, height: 25, color: deepOrange[500]}} /></Tooltip>
      }
      

      let phone_icon;
       if (this.props.user.currentCall.ucid) {
        phone_icon= <PhoneInTalk style={{color: green[500]}} />
        user_icon = <Tooltip title="Talking"><AccountBox style={{ width: 25, height: 25, color: cyan[500]}} /></Tooltip>
       }
         else { phone_icon = <Phone style={{color: red[500]}}/>;
        
        }
      

      //let phonecolor = this.props.user.phoneState === "ACDAVAIL" ? red[500] : green[500];
    
      
      
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