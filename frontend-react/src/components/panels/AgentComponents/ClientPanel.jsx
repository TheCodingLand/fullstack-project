
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



// let defaultStyle = { 
//     color : '#fff' 
//   };



class ClientPanel extends React.Component {

    render () {
      
      
        return(this.props.user.currentCall ?
       <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <div><Typography>{this.props.user.currentCall.origin}</Typography></div><Divider />
        <div><Typography>{this.props.user.currentCall.callType}</Typography></div>

          </Card></div>
          :
          <div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
        <Typography>No Calls in progress</Typography>
        </Card></div>
        ); 
      }
    }



    
    

  export default withTheme()(ClientPanel);