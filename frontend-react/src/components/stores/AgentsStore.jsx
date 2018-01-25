/* STORES: 
- Agents: List of Agents : ID is phone_login, details 
    
Centrale : List of list of centrale users + extentions as ID

Calls : list of calls for extention X calls.login = call : { phone, id, type }

Tickets : List of tickets baed on events Phone number{
  allEvents(phone:"0225626") {
    edges {
      node {
        ticket{
          title
        }
      }
    }
  }
}

*/
import {asyncAction} from "mobx-utils"
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'
import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';


mobx.useStrict(true) // don't allow state modifications outside actions

class RootStore {
    constructor() {
      this.userStore = new UserStore(this)
      this.todoStore = new TodoStore(this)
    }
  }



class Store {
    @observable githubProjects = []
    @observable state = "pending" // "pending" / "done" / "error"



class Store {
        @observable githubProjects = []
        @observable state = "pending" // "pending" / "done" / "error"
    

        fetchConnectedAgents() {
            this.client.cache.reset(); 
            this.client.query({ query: gql`query {
              allAgents(phoneActive: true) {
                edges {
                  node {
                    lastname
                    firstname
                    ext
                    phoneLogin
                    phoneState
                    }
                  }
                }
              }
            }
            ` 
        }
        )

        @asyncAction
        *getConnectedAgents() { // <- note the star, this a generator function!
            this.connectedAgents = []
            this.state = "pending"
            try {
                const projects = yield fetchConnectedAgents() // yield instead of await
                const filteredProjects = somePreprocessing(projects)
                // the asynchronous blocks will automatically be wrapped actions
                this.state = "done"
                this.githubProjects = filteredProjects
            } catch (error) {
                this.state = "error"
            }
        }
    }


class AgentsStore {
    @observable agents = [];
    @observable state = "pending" // "pending" / "done" / "error"
    
    getConnectedAgents() {
        this.connectedAgents = []
        this.state = "pending"

        fetchConnectedAgents(() => {
            this.client.cache.reset(); 
            this.client.query({ query: gql`query {
              allAgents(phoneActive: true) {
                edges {
                  node {
                    lastname
                    firstname
                    ext
                    phoneLogin
                    phoneState
                    }
                  }
                }
              }
            }
            ` }).then(
            action("fetchSuccess", users => {
                const sortedAgents = sortUsers(users)
                runInAction(() => {
                    this.connectedAgents = sortedAgents
                    this.state = "done"
                }),
            // inline created action
            action("fetchError", error => {
                this.state = "error"
            })}
        ))
    }


)}


}



