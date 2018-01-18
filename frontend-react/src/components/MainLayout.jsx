import * as React from 'react';
import { Grid, Cell } from 'styled-css-grid';
import StatsPanel from './panels/StatsPanel';
import MapPanel from './panels/MapPanel';
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
            <Cell width={4}><IncomingPanel queues ={this.props.store.agentStore.queues} /></Cell>
            <Cell width={3}>
                <CSSTransitionGroup transitionName="example" transitionEnterTimeout={2500} transitionLeaveTimeout={2500}>
                    {this.props.store.agentStore.agents && this.props.store.agentStore.agents.map((user) => ( <MainAgentPanelLayout key={user.phoneLogin} user={user}></MainAgentPanelLayout>))}
                </CSSTransitionGroup>
            </Cell>
            <Cell width={1} height={2}>
                <Grid columns={1}>
                    {//<Cell width={1} height={1}><StatsPanel/></Cell>}
                    }
                    {//<Cell width={1} height={1}><MapPanel/></Cell>
                    }
                </Grid>
            </Cell>
        </Grid>
        );
    };
}
/* <CSSTransitionGroup
                        transitionName="example"
                        transitionEnterTimeout={2500}
                        transitionLeaveTimeout={2500}>
                          </CSSTransitionGroup> */