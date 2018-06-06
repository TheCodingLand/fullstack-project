import React from 'react';
import PropTypes from 'prop-types';
import Downshift from 'downshift';
import { withStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import MenuItem from '@material-ui/core/MenuItem';




function getSuggestions(suggestions, inputValue) {
  let count = 0;
  
  let values = suggestions.filter(suggestion => {
    const keep =
      (!inputValue || suggestion.label.toLowerCase().indexOf(inputValue.toLowerCase()) !== -1) &&
      count < 5;

    if (keep) {
      count += 1;
    }

    return keep;
  });

  return values
}

function renderInput(inputProps) {
  const { InputProps, classes, ref, ...other } = inputProps;

  return (
    <TextField
      
      InputProps={{
        inputRef: ref,
        classes: {
          
         
        },
        ...InputProps,
      }}
      {...other}
    />
  );
}

function renderSuggestion({ suggestion, index, itemProps, highlightedIndex, selectedItem }) {
  const isHighlighted = highlightedIndex === index;
  const isSelected = (selectedItem || '').indexOf(suggestion.label) > -1;

  return (
    <MenuItem
      {...itemProps}
      key={suggestion.label}
      selected={isHighlighted}
      component="div"
      style={{
        fontWeight: isSelected ? 500 : 400,
      }}
    >
      {suggestion.label}
    </MenuItem>
  );
}
renderSuggestion.propTypes = {
  highlightedIndex: PropTypes.number,
  index: PropTypes.number,
  itemProps: PropTypes.object,
  selectedItem: PropTypes.string,
  suggestion: PropTypes.shape({ label: PropTypes.string }).isRequired,
};



const styles = theme => ({
  root: {
    flexGrow: 1,
    height: 250,
  },
  container: {
    witdth:800,
    flexGrow: 1,
    position: 'relative',
  },
  paper: {
    position: 'absolute',
    zIndex: 1,
    marginTop: theme.spacing.unit,
    left: 0,
    right: 0,
  },
  chip: {
    margin: `${theme.spacing.unit / 2}px ${theme.spacing.unit / 4}px`,
  },
  inputRoot: {
    flexWrap: 'wrap',
   
  },
});

class CategoriesSelect extends React.Component {

  
  suggestions = this.props.categories.map((category) => { return { label: category.title} } )
  
  state = {
    inputValue: '',
    selectedItem: [],
  };

  render() {
  const { classes } = this.props;
//  const { inputValue, selectedItem } = this.state;
  return (
    <div className={classes.root}>
      <Downshift onSelect={this.props.onSelect}>
        {({ getInputProps, getItemProps, isOpen, inputValue, selectedItem, highlightedIndex }) => (
          <div className={classes.container}>
            {renderInput({
              fullWidth: true,
              InputProps: getInputProps({
                placeholder: 'Search a category',
                id: 'integration-downshift-simple',
              }),
            })}
            {isOpen ? (
              <Paper className={classes.paper} square>
                {getSuggestions(this.suggestions,inputValue).map((suggestion, index) =>
                  renderSuggestion({
                    suggestion,
                    index,
                    itemProps: getItemProps({ item: suggestion.label }),
                    highlightedIndex,
                    selectedItem,
                  }),
                )}
              </Paper>
            ) : null}
          </div>
        )}
      </Downshift>
      
    </div>
  );
}
}

CategoriesSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CategoriesSelect);