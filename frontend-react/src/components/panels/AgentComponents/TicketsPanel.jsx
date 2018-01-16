import * as React from 'react';
import Typography from 'material-ui/Typography';
import Card from 'material-ui/Card'
import { withTheme } from 'material-ui/styles';
import { observer } from "mobx-react";


// let defaultStyle = { 
//     color : '#fff' 
//   };

@observer
class TicketsPanel extends React.Component {
    render () {
      if (this.props.user.currentCall.tickets) {
        console.log(this.props.user.currentCall)
        if (this.props.user.currentCall.tickets.length > 0){
          console.log(this.props.user.currentCall.tickets)
          
        return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
       <Typography>Tickets precedents de ce client :</Typography>
       {this.props.user.currentCall.tickets.map((ticket) => ( function (){ if (ticket.category.title) { <Typography key={ticket.otId}>{ticket.title}, category :{ticket.category.title} </Typography>}}))}
        </Card></div> )
        } 
          else
          {
            return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
            <Typography></Typography>
            </Card></div>)
          }
        }
        else{
          return(<div><Card style={{ overflowX: 'hidden', flex: 'auto', height: "90px", width:"100%" }}> 
          <Typography></Typography>
          </Card></div>)

        }}
        
      }
    



  

    

  export default withTheme()(TicketsPanel);