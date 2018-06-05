import * as React from 'react';
import { Grid, Cell } from 'styled-css-grid';
import MainAgentPanelLayout from './panels/MainAgentPanelLayout';
import { CSSTransitionGroup } from 'react-transition-group';
import "./MainLayout.css"
import { observer } from "mobx-react";
import IncomingPanel from './panels/IncomingPanel'


var letterStyle = {
    padding: 10,
    margin: 10,
    fontFamily: "Roboto",
    fontSize: 14,
    textAlign: "center"
  };

  @observer
export default class MainLayout extends React.Component {
    render() { 

        return(
        <Grid style={letterStyle} columns={4}>
            <Cell width={4}><IncomingPanel categories={this.props.categories} store={this.props.store} agents={this.props.store.agentStore.agents}/></Cell>
            <Cell width={4}>
                <CSSTransitionGroup transitionName="example" transitionEnterTimeout={2500} transitionLeaveTimeout={2500}>
                    {this.props.store.agentStore.agents && this.props.store.agentStore.agents.map((user) => ( <MainAgentPanelLayout key={user.phoneLogin} user={user}></MainAgentPanelLayout>))}
                </CSSTransitionGroup>
            </Cell>
         
        </Grid>
        
        );
    };
}
