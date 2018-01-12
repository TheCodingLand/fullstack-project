
import { graphql } from 'react-apollo'
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

async ListAgents() {
   
    console.log("retrieving agents from server")
    this.client.cache.reset(); 
    
    let data = await this.client.query({ query: gql`query {
      allAgents(phoneActive: true) {
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
      }
    
        ` })
        return data
       }



async GetAgent(login) {
   
    console.log("retrieving agents from server")
    this.client.cache.reset(); 
    
    let data = await this.client.query({ query: gql`query {
          allAgents(phoneLogin: "${login}") {
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
        }
        ` })
        return data
       }

  async GetCall(ucid) {
        console.log("retrieving agents from server")
        this.client.cache.reset(); 
        
        let data = await this.client.query({ query: gql`query {
              allCalls(ucid: "${ucid}") {
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

}
