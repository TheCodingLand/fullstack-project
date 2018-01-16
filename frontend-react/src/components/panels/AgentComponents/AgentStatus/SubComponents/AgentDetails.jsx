import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card from 'material-ui/Card';
import CardHeader from 'material-ui/Card/CardHeader';
import Avatar from 'material-ui/Avatar';
import { withTheme } from 'material-ui/styles';
import MailIcon from 'material-ui-icons/Mail';
import Badge from 'material-ui/Badge';
// let defaultStyle = { 
//     color : '#fff' 
//   };
class AgentDetails extends React.Component {
    render () {
      const { theme } = this.props;
    
      const primaryColor = theme.palette.primary[500];
    
      // const styles = {
      //   primaryText: {
      //     backgroundColor: theme.palette.background.default,
      //     padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`,
      //     color: primaryText,
      //   },
      //   primaryColor: {
      //     backgroundColor: primaryColor,
      //     padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`,
      //     color: '#fff',
      //   },
      // };
      
      let hr = <CardHeader
      avatar={ <Avatar style={{color: '#fff', backgroundColor : primaryColor}} aria-label="firstname">X</Avatar>}

      title="Loading"
      />



      if (this.props.user) { 
        if (this.props.user.firstname) {
       hr =<div><CardHeader
      avatar={ <Avatar style={{color: '#fff', backgroundColor : primaryColor}} aria-label="firstname">{this.props.user.firstname.charAt(0)}</Avatar>}

      title={this.props.user.firstname}
      subheader={this.props.user.lastname}

/></div>
      }
    }

      //let phonecolor = this.props.user.phoneState === "ACDAVAIL" ? red[500] : green[500];
    
      
      
      return(this.props.user ?
      <div><Card style={{ flex: 'auto', height: "90px" }}> {hr}<Badge style={{ top: "-51px", left: "135px"}} badgeContent={4} color="accent">
      <MailIcon style={{ width: 10, height:10}} />
    </Badge></Card></div>  :
      <Typography>loading Agent</Typography>
      ); 
    }
  };




 export default withTheme()(AgentDetails);





      // let classname = this.props.user.phoneState === "ACDAVAIL" ? "agentactive" : "agentinactive";
      // return(this.props.user ? 
      //   <div style={{display:"flex"}} className={classname}>
      //     <div style={{paddingRight:"10px"}}>
      //     <h3>{this.props.user.firstname}</h3></div>
      //     <div>
      //     <h3>{this.props.user.ext}</h3>
      //   </div>
      //   </div> :
      //   <h3>loading users</h3>
  //     ); 
  //   }
  // }
  
  // export default class AgentStats extends React.Component {
    
  //   render () {
  //     //let phonecolor = this.props.user.phoneState === "ACDAVAIL" ? red[500] : green[500];
  //     let phonecolor = this.props.user.currentCall ? red[500] : green[500];
  //     let icon = this.props.user.currentCall ? <PhoneInTalk style={{color: green[500]}} /> :<Phone style={{color: red[500]}}/> ;
  //     console.log(this.props.user.phoneState);
  //     return(this.props.user ?
  //     <div><Card style={{height: "100px"}}> <Typography>{this.props.user.phoneLogin}</Typography><div>
  //     <Typography>{this.props.user.firstname}</Typography></div>{icon}</Card></div>  :
  //     <Typography>loading Agent</Typography>
  //     ); 
  //   }
  // }