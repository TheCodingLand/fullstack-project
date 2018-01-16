import * as React from 'react';
//import AgentList from "./components/TodoList";
import Reboot from 'material-ui/Reboot';
import RootStore from "./models/RootStore";
import MainLayout from './components/MainLayout'
//<MainLayout users={this.state.serverData.users}/> 

import DevTools from 'mobx-react-devtools';



class App extends React.Component {
  constructor() {
    super();
    this.store = new RootStore();
    this.store.agentStore.GetAgentList()

  }

render() {
    return(
      <div>
        <DevTools />
     <Reboot />
     
      
      <MainLayout store={this.store}/> 
      </div>
    
     )
  }
    
  
}

//<AgentList store={this.store} />

export default App;