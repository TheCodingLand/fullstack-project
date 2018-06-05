import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card'
import { withTheme } from '@material-ui/core/styles';
import { observer } from "mobx-react";
import MailIcon from '@material-ui/icons/Mail';
import Badge from '@material-ui/core/Badge';



@observer
class TicketsPanel extends React.Component {
  render() {
   
      if (this.props.user.currentCall.origin ==="False"){
      return (<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>
          <Typography>Unknown client call. Your stats : </Typography><p></p><Badge badgeContent={this.props.user.totalcalls?this.props.user.totalcalls:"0"} color="secondary"><MailIcon style={{ width: 10, height: 10 }} /></Badge>
        </Card></div>)
    }
      else
    {
    if (this.props.user.currentCall.tickets) {

      if (this.props.user.currentCall.tickets.length > 0) {

        let tickets = []
        for (let i = 0; i < this.props.user.currentCall.tickets.length; i++) {

          if (this.props.user.currentCall.tickets[i]) {
            let ticket = this.props.user.currentCall.tickets[i]
            if (ticket.title) {
              tickets.push(ticket)
            }
          }
        }
        tickets = tickets.slice(-3)
        return (<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>

          {tickets.map((ticket) => (<Typography key={ticket.otId}><b>Ticket : </b>{ticket.title}</Typography>))}
        </Card></div>)
      }
      else {
        return (<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>
          <Typography>your current stats :</Typography><p></p><Badge badgeContent={this.props.user.totalcalls?this.props.user.totalcalls:"0"} color="secondary"><MailIcon style={{ width: 10, height: 10 }} /></Badge>
        </Card></div>)
      }
    }

    else {
      return (<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>
        <Typography>your current stats :</Typography><p></p><Badge badgeContent={this.props.user.totalcalls?this.props.user.totalcalls:"0"} color="secondary"><MailIcon style={{ width: 10, height: 10 }} /></Badge>


      </Card></div>)

    }
  }

  }

}








export default withTheme()(TicketsPanel);