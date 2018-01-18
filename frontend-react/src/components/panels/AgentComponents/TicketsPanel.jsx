import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card from 'material-ui/Card'
import { withTheme } from 'material-ui/styles';
import { observer } from "mobx-react";
import MailIcon from 'material-ui-icons/Mail';
import Badge from 'material-ui/Badge';

// let defaultStyle = { 
//     color : '#fff' 
//   };

@observer
class TicketsPanel extends React.Component {
    render () {
      if (this.props.user.currentCall.tickets) {
        //console.log(this.props.user.currentCall)
        if (this.props.user.currentCall.tickets.length>0){
          
          //console.log(this.props.user.currentCall.tickets[0].category.title)
          let tickets =[]
          for (let i = 0; i < this.props.user.currentCall.tickets.length; i++) 
          {
            let t
            if (this.props.user.currentCall.tickets[i]) {
            let ticket = this.props.user.currentCall.tickets[i]
            console.log (ticket.title)
            if (ticket.title) {
              console.log (ticket)
               tickets.push(ticket)
            }
          }
          }
        tickets.slice(-3)
        return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
      
      
       {tickets.map((ticket) => ( <Typography key={ticket.otId}>{ticket.title}</Typography>))}
        </Card></div> )
        
        }
        else
          {
            return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
           <Typography>your current stats :</Typography><p></p><Badge badgeContent={4} color="accent"><MailIcon style={{ width: 10, height:10}} /></Badge>
            </Card></div>)
          }
        }

        else{
          return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
          <Typography>your current stats :</Typography><p></p><Badge badgeContent={4} color="accent"><MailIcon style={{ width: 10, height:10}} /></Badge>

          
          </Card></div>)

        }
      
      
    }
        
}
    



  

    

  export default withTheme()(TicketsPanel);