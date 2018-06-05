import * as React from 'react';
import Typography from '@material-ui/core/Typography';
export default class Version extends React.Component {

    render() { 
    
    return (<div style={{position:'absolute', right:0,bottom:0}}><Typography>version {this.props.version}</Typography></div>)
    }



}
