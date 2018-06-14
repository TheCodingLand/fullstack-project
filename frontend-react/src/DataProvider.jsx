
import gql from 'graphql-tag'
import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';






export default class DataProvider {
  constructor() {


    this.client = new ApolloClient({
      link: new HttpLink({ uri: 'http://148.110.107.15:8099/graphql' }),
      cache: new InMemoryCache()
    });

  }

  /* async ListAgents() {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`query {
      allAgents(phoneActive: true) {
        edges {
          node {
            id
            lastname
            firstname
            ext
            phoneLogin
            phoneState
            otUserdisplayname
            currentCall{
              ucid
              origin
              start
              destination
              callType 
            }
            }
          }
        }
      }
    
        ` })
    return data
  } */

  async ListAgents() {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`query {
      allAgents(phoneActive: true) {
        edges {
          node {
            id
            lastname
            firstname
            ext
            phoneLogin
            phoneState
            otUserdisplayname
          
            }
          }
        }
      }
    
        ` })
    return data
  }



  async GetAgent(login) {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`query {
          allAgents(phoneLogin: "${login}") {
            edges {
              node {
                id
                lastname
                firstname
                ext
                phoneLogin
                phoneState
                otUserdisplayname
              }
            }
          }
        }
        ` })
    return data
  }

  async GetCall(ucid) {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`query {
            allCalls (ucid:"${ucid}") {
              edges {
                node {
                  ucid
                  origin
                  start
                  destination
                  callType
                }
              }
            }
            }
         ` })
    return data

  }

 /*  async getQueueLines(line) {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`{allAgents(isQueueLine:true){
        edges {
          node {
            id
            lastname
            firstname
            ext
            phoneLogin
            phoneState
            currentCall{
              ucid
              origin
              start
              destination
              callType 
            }
            }
          }
        }
      }`})
  return data
} */

async getQueueLines(line) {
  this.client.cache.reset();

  let data = await this.client.query({
    query: gql`{allAgents(isQueueLine:true){
      edges {
        node {
          id
          lastname
          firstname
          ext
          phoneLogin
          phoneState
         
          }
        }
      }
    }`})
    
return data
}


  async getIncomingCallByLine(line) {
    this.client.cache.reset();

    let data = await this.client.query({
      query: gql`query {
    allCalls (destination:"${line}",state:"new") {
edges{
node{
  callType
  state
  origin
}
}     
}
}`})

    return data
  }
  async getTicketbyPhone(phone) {
    this.client.cache.reset();
    let datestart = new Date(Date.now()).toISOString()
    let start = datestart.slice(0,10)
    let data = await this.client.query({

      query: gql`query {  
              allEvents(phone:"${phone}", end_Gte:"${start}") {
                edges {
                  node {
                    id
                    phone
                    ticket{
                      otId
                      title
                      solution
                      category {
                        otId
                        title
                      }           
                    }
                  }
                }
              }
            }
          `
    })
  
    return data
  }

  async getCallsbyAgentExt(phone) {
    this.client.cache.reset();
    let datestart = new Date(Date.now()).toISOString()

    let start = datestart.slice(0,10)
    let data = await this.client.query({
      query: gql`query {  
        allCalls (start_Gte:"${start}",destination:"${phone}"){
          edges
      {
      node{
        ucid
           }
        }
      }
    }`
    })
    
    return data
    
  } 

  async getActiveCalls(phone) {
    this.client.cache.reset();
    let data = await this.client.query({
      query: gql`query
  {
    allCalls(state: "new") {
      edges {
        node {
          ucid
          start
          origin
          destination
          callType
        }
      }
    }
  }`
})
return data
  }

  
  async getEventsbyAgentExt(phone) {
    this.client.cache.reset();
    let datestart = new Date(Date.now()).toISOString()

    let start = datestart.slice(0,10)
    let data = await this.client.query({
      query: gql`query {  
          allCalls(start_Gte:"${start}",destination:"${phone}") {
            edges {
              node {
                ucid
                start
                origin
                event {
                  edges {
                    node {
                      otId
                      ticket {
                        otId
                      }
                    }
                  }
                }
              }
            }
          }
        }
        `
    })
    return data
  }
}

