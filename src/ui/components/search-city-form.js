import React, { Component } from 'react';
import './search-city-form.less';
class SearchCityForm extends Component {
  constructor (props) {
    super(props);
  }

  state = {
    cityName: '',
    date: new Date(),
  }

  handleChangeCity = (event) => {
    this.setState({ cityName: event.target.value });
  }
  handleChangeDate = (event) => {
    this.setState({ date: event.target.value });
  }

  searchCity = (event) => {
    event.preventDefault();
    event.stopPropagation();
    if (this.state.cityName) {
      this.props.searchCity(this.state.cityName);
    }
  }

  iconClassName = () => {
    const { isSearching, hasError } = this.props;

    if (isSearching) return "fas fa-spinner fa-spin icon";
    if (hasError) return "fas fa-times icon";
    return "fas fa-search icon";
  }

  render () {
    return (
      <form className="search-form" onSubmit={this.searchCity}>
        <h4 className="title">
          Add flood predictions for a new location
        </h4>
        <div className="search-box">
          <input className="input-search" type="text" placeholder="Name of City"
            value={this.state.cityName} onChange={this.handleChangeCity}
            // ref={(ref) => { ref && setTimeout(() => { ref.focus() }); }} autoFocus 
            />
          <input type="date" value={this.state.date} onChange={this.handleChangeDate}
            className="input-date"
          //  ref={(ref) => { ref && setTimeout(() => { ref.focus() }); }} autoFocus
          />
          <br/>
          <button className="button-search" type="submit" onClick={this.searchCity}>
            <i className={this.iconClassName()} />
            <span>Search</span>
          </button>
        </div>
      </form>
    );
  }
}

export default SearchCityForm;
