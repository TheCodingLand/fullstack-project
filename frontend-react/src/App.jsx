import * as React from 'react';
import MainLayout from './components/MainLayout'
//import styled from "styled-components";
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import Websocket from 'react-websocket';
import { socketConnect } from 'socket.io-react';
import io from 'socket.io-client';
import Reboot from 'material-ui/Reboot';

class App extends React.Component {
  constructor () {
    super();
     this.client = new ApolloClient({
       link: new HttpLink({ uri: 'http://148.110.107.15:8099/graphql' }),
       cache: new InMemoryCache()
     });
    
    this.state ={ serverData : {} };
    let SOCKET_URL = "localhost:3002"
    this.socket = io.connect(SOCKET_URL);
    this.lastUpdate = Date.now();
    
    console.log(this.socket)
  };


   handleData(data) {
     let result = JSON.parse(data);
   console.log(result);
   }

   onDataRecieved (data) {

    var listofusers = [];
    if (data.data.allAgents) { listofusers = data.data.allAgents.edges.map((edge) => { return edge.node })}
    var users = { users : listofusers }
    this.setState( { serverData : { users : users.users } })
   } 
  
   updateData (data) { 
     
    if (Date.now()- this.lastUpdate > 300){
    this.lastUpdate = Date.now()
    this.client.cache.reset(); 
    this.client.query({ query: gql`query {
      allAgents(phoneActive: true) {
        edges {
          node {
            id
            lastname
            firstname
            ext
            phoneLogin
            phoneState
            currentCall {
              callType
              ucid
              origin
              destination
            }
          }
        }
      }
    }
    ` }).then(this.onDataRecieved.bind(this))
   }
  
  }

  componentDidMount() {
    //first query to refresh
    
    this.updateData();
    this.socket.on('message',((data) =>  { this.updateData(data)})  );
    
    
  }



  render() {
    return(
      <div>
     <Reboot />
     
      <MainLayout users={this.state.serverData.users}/> 
      
      </div>
    
     )
  }
    
  }


export default App;
