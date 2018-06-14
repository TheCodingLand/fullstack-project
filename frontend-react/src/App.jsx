import * as React from 'react'

//import AgentList from "./components/TodoList";
import CssBaseline from '@material-ui/core/CssBaseline'
import RootStore from "./models/RootStore"
import MainLayout from './components/MainLayout'
//<MainLayout users={this.state.serverData.users}/> 
import Loader from './components/Loader'
import response from './categories'
import Version from './components/Version'
import green from '@material-ui/core/colors/green';
import purple from '@material-ui/core/colors/purple';
import red from '@material-ui/core/colors/red';
import Button from '@material-ui/core/Button';
//import Perf from 'react-addons-perf'; // ES6

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { dark } from '@material-ui/core/styles/createPalette';

const themeDark = createMuiTheme({
  typography: {
    fontWeightLight: 200,
    fontWeightRegular: 200,
    fontWeightMedium: 300
  },


  palette: {
    type: 'dark',
    primary: purple, // Purple and green play nicely together.
    secondary: {
      ...green,
      A400: '#00e677',
    },
    error: red,
  },
});

const themeLight = createMuiTheme({
  typography: {
    fontWeightLight: 500,
    fontWeightRegular: 600,
    fontWeightMedium: 800
  },


  palette: {
    type: 'light',
    primary: purple,
    secondary: {
      ...green,
      A400: '#00e677',
    },
    error: red,
  },
});


class App extends React.Component {
  version = "1.2"

  constructor() {
    super();
    this.store = new RootStore();
    this.store.agentStore.GetAgentList()
    this.store.agentStore.GetQueuesList()
    this.store.agentStore.getActiveCalls()
    

    //this.getCategories().then(
    //    (categories) => categories.filter(category => category.state === "Active")).then(
    //        (categories) => this.setState({categories:categories}))
    
  }
  

  state = {
    categories : [],
    loaded:false,
    
    themeName:"light",
    theme:themeLight

  }
  setTheme = () => () => {
    if (this.state.themeName==="light") {
      this.setState({theme:themeDark, themeName:"dark"})

    }
    else {
      this.setState({theme:themeLight, themeName:"light"})
    }
  }
  componentWillMount(){
    this.getCategoriesFromResponseFile()
   // setInterval(()=> {console.log(this.store)},5000)
  }
  getCategoriesFromResponseFile(){
    let catlist = response.Category.map(category => { return { id: category.id, title : category.data.Path, state : category.data.State}  })
    catlist = catlist.filter(category => category.state === "Active")
    this.setState({categories:catlist})
    
  }



  getCategories() {
    

    let query = {
      
        objectclass: "Category",
        filter: "",
        variables: [
        ],
        requiredfields: [
          "Path",
          "State"
        ]
    }
      return fetch('http://148.110.107.15:5001/api/ot/objects', {
          method: 'POST',
          body: JSON.stringify(query),
          headers: { 'Accept': 'application/json',
          'Content-Type': 'application/json'}
      }
      ).then(response => response.json()
          ).then(
              (response) => response.Category.map( (category) => {  return { id: category.id, title : category.data.Path, state : category.data.State} } ) )
    }

    
  

render() {
  
  //Perf.start()
    return(
      <MuiThemeProvider theme={this.state.theme}>
      <div>
      <Button onClick={this.setTheme('light')} > changetheme </Button>
       
     <CssBaseline  />
     <Version version ={this.version}/>
     {this.state.categories!==[]?<MainLayout categories={this.state.categories} store={this.store}/>:<Loader /> 
    }
    
     </div>
     </MuiThemeProvider>
     )
//     Perf.stop()
  }
}

//<AgentList store={this.store} />

export default App;