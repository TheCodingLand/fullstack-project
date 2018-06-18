import * as React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card'
import { withTheme } from '@material-ui/core/styles';
import { observer } from "mobx-react";
import MailIcon from '@material-ui/icons/Mail';
import Badge from '@material-ui/core/Badge';
import Button from '@material-ui/core/Button'


@observer
class TicketsPanel extends React.Component {
  transferTicket= ticket => {
    console.log("transfering ticket "+  ticket.otId + "  to " + ticket.tickets.edges[0].node.applicant.otUserdisplayname)
    let query= {
      Responsible: 'Lebourg Julien',
    }
    return fetch('http://148.110.107.15:5001/api/ot/ticket', {
      method: 'PUT',
      body: JSON.stringify(query),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(this.props.user.getTickets())
   
    
  }

  render() {
    let tickets= []
    if (this.props.user.currentUser===true){ 
     
      this.props.user.tickets.forEach(ticket => { 
        
        if (ticket.tickets.edges[0].node.applicant.phoneLogin){
        if (ticket.tickets.edges[0].node.applicant.phoneLogin!==this.props.user.phoneLogin)
        {

          tickets.push(<div>{ticket.creationdate + " " + ticket.title + " "}<Button onClick={() => this.transferTicket(ticket)}> transfer ticket to {ticket.tickets.edges[0].node.applicant.firstname}? </Button></div>) 
        }
        
    }
  }
    )

    

    }
      if (this.props.user.currentCall.origin ==="False"){
      return (<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width: "100%" }}>
          <Typography>Unknown client call.</Typography><p></p><Badge badgeContent={this.props.user.totalcalls?this.props.user.totalcalls:"0"} color="secondary"><MailIcon style={{ width: 10, height: 10 }} /></Badge>
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
        <Typography>{tickets}</Typography><p></p><Badge badgeContent={this.props.user.totalcalls?this.props.user.totalcalls:"0"} color="secondary"><MailIcon style={{ width: 10, height: 10 }} /></Badge>


      </Card></div>)

    }
  }

  }

}








export default withTheme()(TicketsPanel);