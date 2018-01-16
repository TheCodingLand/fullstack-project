import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { LinearProgress } from 'material-ui/Progress';


const styles = {
  root: {
    width: '100%',
    marginTop: 30,
  },
};

class ProgressBar extends React.Component {
  state = {
    completed: 0,
  };

  componentDidMount() {
    this.timer = setInterval(this.progress, 500);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  

  progress = () => {
    const { completed } = this.state;
    if (completed > 100) {
      this.setState({ completed: 0 });
    } else {
      const diff = .5;
      this.setState({ completed: completed + diff });
    }
  };

  render() {
    const { classes } = this.props;
    return (
        
      <div className={classes.root}>
        
        
        <LinearProgress color="accent" mode="determinate" value={this.state.completed} />
        
      </div>
    
    );
  }
}

ProgressBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ProgressBar);