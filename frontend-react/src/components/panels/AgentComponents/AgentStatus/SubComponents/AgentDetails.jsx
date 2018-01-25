import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card from 'material-ui/Card';
import CardHeader from 'material-ui/Card/CardHeader';
import Avatar from 'material-ui/Avatar';
import { withTheme } from 'material-ui/styles';


class AgentDetails extends React.Component {
    render () {
      const { theme } = this.props;
    
      const primaryColor = theme.palette.primary[500];
    
    
      
      let hr = <CardHeader
      avatar={ <Avatar style={{color: '#fff', backgroundColor : primaryColor}} aria-label="firstname">X</Avatar>}

      title="Loading"/>

      if (this.props.user) { 
        if (this.props.user.firstname) {
       hr =<div><CardHeader
      avatar={ <Avatar style={{color: '#fff', backgroundColor : primaryColor}} aria-label="firstname">{this.props.user.firstname.charAt(0)}</Avatar>}

      title={this.props.user.firstname}
      subheader={this.props.user.lastname}

/></div>
      }
    }
      return(this.props.user ?
      <div><Card style={{ flex: 'auto', height: "90px" }}> {hr}</Card></div>  :
      <Typography>loading Agent</Typography>
      ); 
    }
  };


 export default withTheme()(AgentDetails);
