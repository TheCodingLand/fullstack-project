
import React from 'react';

import { withStyles } from '@material-ui/core/styles';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import { observer } from "mobx-react";
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import CategoriesSelect from './CategoriesSelect';
import ClientForm from './ClientForm';
import purple from '@material-ui/core/colors/purple';
import Client from '../../../models/ClientModel'
import { RingLoader } from 'react-spinners';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  selects:{
    marginLeft: theme.spacing.unit,
  },
  resultField:{
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: '100',
  },
  textField: {

    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: '90%',
  },
 
  categoryField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 800,
  },
  menu: {
    width: 200,
  },
  cssRoot: {
    color: theme.palette.getContrastText(purple[500]),
    backgroundColor: purple[500],
    '&:hover': {
      backgroundColor: purple[700],
    },
  }
});


@observer
class TicketForm extends React.Component {
  suggestions = this.props.categories.map((category) => { return { label: category.title, id: category.id } })
  state = {
    event: '',
    title: '',
    description: '',
    solution: '',
    category: '',
    origin: '',
    client: '',
    events: this.props.agent.callsWithoutTickets,
    selectedEvent: {},
    response: {},
    possibleClients:[],
    selectedClient:{ otId:"", FirstName: "", LastName:""},
    clientsLoaded : false,
    savedClientID:""

  }

  makeTicketSolved(response) {
  


      let query = {
        State: "Solved"
      }

      return fetch('http://148.110.107.15:5001/api/ot/ticket/' + response.ticket, {
        method: 'PUT',
        body: JSON.stringify(query),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json()).then(() => this.linkEventToTicket(response.ticket, this.state.selectedEvent.otId))

    }
  

  linkEventToTicket(ticketid, eventid) {
    let query = {
      RelatedIncident: ticketid
    }

    return fetch('http://148.110.107.15:5001/api/ot/event/' + eventid, {
      method: 'PUT',
      body: JSON.stringify(query),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }
    ).then(response => response.json()).then(response => this.setState({ response: response })).then(() => this.props.agent.callsWithoutTickets.remove(this.state.selectedEvent)).then(
      () => this.props.store.updatePendingTickets(this.state.selectedEvent.otId)).then(() =>

        this.setState({
          event: '',
          title: '',
          description: '',
          solution: '',
          category: '',
          origin: '',
          client: '',
          selectedEvent: {}
        }))
  }

  selectClient = name => client => {
    this.setState({selectedClient: client})
    console.log(client)
  }
    
  


  handleChangeCategory = name => title => {
    this.props.categories.forEach((category) => {
      if (category.title === title) {
        this.setState({ category: category.id })
      }
    })
  }


/*   makeTicketSolved(response) {
  


    let query = {
      State: "Solved"
    }

    return fetch('http://148.110.107.15:5001/api/ot/ticket/' + response.ticket, {
      method: 'PUT',
      body: JSON.stringify(query),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json()).then(() => this.linkEventToTicket(response.ticket, this.state.selectedEvent.otId))

  } */

  
  saveClient(){
    
    


    return fetch('http://148.110.107.15:5001/api/ot/clients', {
      method: 'PUT',
      body: JSON.stringify({FirstName:this.state.selectedClient.FirstName, LastName:this.state.selectedClient.LastName}),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json()).then(response => {
        if (response.status === 'success') {
          this.setState({savedClientID:response.ticket})
      
        }
        else{
          this.setState({savedClientID:""})
        }
      
      })
  


}




  
    
    
  
 

  
  handleTicketSubmit = (e) => {
    console.log(this.state.selectedClient)
    if (this.state.selectedClient.otId === "" && this.state.selectedClient.LastName!=="") {
       
      this.saveClient().then(() => this.saveTicket())
      }
    
    else
    {
    this.saveTicket()
    }
  }

    saveTicket = () => {
    {

      let ticket = {
        Title: this.state.title,
        Description: this.state.description,
        SolutionDescription: this.state.solution,
        AssociatedCategory: this.state.category,
        Applicant: this.props.agent.otUserdisplayname,
        Responsible: this.props.agent.otUserdisplayname,
      }

    if (this.state.savedClientID !== ""){

      ticket.ReportingPerson = this.state.savedClientID 
      console.log(ticket.ReportingPerson)
    
    }
    else if (this.state.client.otId !=="")
    {

      ticket.ReportingPerson = this.state.selectedClient.otId
    
    }
  
    return fetch('http://148.110.107.15:5001/api/ot/tickets', {
      method: 'PUT',
      body: JSON.stringify(ticket),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json()).then(response => { if (response.status ==='success') { this.makeTicketSolved(response)} else {this.setState({response:response})}})
    }
  }

  //getEvents() {
  //  this.setState({ events: this.props.agent.callsWithoutTickets })
  //}

  componentDidMount() {
    //this.getEvents()

  }

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    }
    )
  }
  

  handleEventChange = name => event => {
    
    this.setState({
      [name]: event.target.value,
    });
    this.state.events.forEach((e) => {
      if (e) {
        if (e.id === event.target.value) {
          if (e.origin) {
            if (e.origin.charAt(0) === '0') {
                e.origin = e.origin.substr(1);
            }
            
        }
          this.setState({ selectedEvent: e, origin: e.origin })
          this.setState({clientsLoaded:false})
          this.getPossibleClients(e.origin).then(() => this.setState({clientsLoaded:true}))
        }
      }
    })}

  

  getPossibleClients(phone) {
    if (phone.length > 3){

        let query = {
    
            objectclass: "Client",
            filter: "ClientFromPhone",
            variables: [
                {
                    name: "phone",
                    value: phone,
                    //value: "4634637941"
                }
            ],
            requiredfields: [
    
            ]
        }
        //console.log(query)
        return fetch('http://148.110.107.15:5001/api/ot/objects', {
            method: 'POST',
            body: JSON.stringify(query),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }
        ).then(response => response.json()
        ).then(
            (response) => {
                if (response.status === "success") {
                    //console.log(response.Client)
    
                    let clients = response.Client.map((client) => { return new Client(client) })
                    this.setState({possibleClients : clients})
                }
                else {
                   this.setState({possibleClients : [ ]})
                }
            }
        )
    }
    else {
        this.setState({possibleClients : [ ]})
    }
}
  
  render() {
    let menuitems = []
    if (this.state.events.length > 0) {
      menuitems = this.state.events.map((event) => {  return <MenuItem key={event.id} origin={event.origin} value={event.id}>{event.start}</MenuItem> } )
    }
    else {
      menuitems = [<MenuItem key={1} origin="nothing" value="None">None</MenuItem>,]
    }
    const { classes } = this.props;

    return (<div>
      <form className={classes.container} noValidate autoComplete="off">
      
          <FormControl fullWidth={true} className={classes.selects}>
            <InputLabel htmlFor="event">Event</InputLabel>

            <Select className={classes.selects}
              required
              value={this.state.event}

              onChange={this.handleEventChange('event')}

            >
              {menuitems}
            </Select>
            <FormHelperText>Select your Event</FormHelperText>
          </FormControl>
      

        <TextField
          id="origin"
          label="call origin"
          className={classes.textField}
          margin="normal"
          disabled
          onChange={this.handleEventChange('origin')}
          value={this.state.origin}
        />
        {this.state.clientsLoaded?
        <ClientForm selectedClient={this.state.selectedClient} onClientSelect={this.selectClient('client')} possibleClients={this.state.possibleClients}/>
        :
        <div className='sweet-loading'>
        <RingLoader
          color={'#123abc'} 
          
        />
      </div>
        }

       
        <TextField
          required
          id="title"
          label="Title"
          className={classes.textField}
          margin="normal"
          onChange={this.handleEventChange('title')}
        />

        

        <TextField
          required
          multiline
          id="description"
          label="Description"
          className={classes.textField}
          margin="normal"
          rowsMax="4"
          onChange={this.handleChange('description')}
        />
        <br />
        <TextField
          required
          rowsMax="4"
          id="solution"
          label="Solution"
          className={classes.textField}
          margin="normal"
          multiline
          
          onChange={this.handleChange('solution')}
        />
        <div className = {classes.selects} style={{width:'800px'}}>
       
        <CategoriesSelect categories={this.props.categories}
          required
          onSelect={this.handleChangeCategory()}
          
        />
        
        </div>
        <div style={{width:'100%'}}>
        
        <Button className={classes.cssRoot} variant="raised" color="primary" onClick={this.handleTicketSubmit}>Valider</Button>
        <TextField
          color="secondary"
          disabled
          id="response"
          label="response"
          className={classes.resultField}
          
          margin="normal"
          rowsMax="4"
          value={this.state.response.status ? this.state.response.status : "none"}

        />
       </div>
      </form>
    </div>
    )

  }
}

export default withStyles(styles)(TicketForm);
