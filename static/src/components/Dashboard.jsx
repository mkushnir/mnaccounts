import React from 'react';

//import {
//  formatMessage,
//} from 'devextreme/localization';

// https://js.devexpress.com/Demos/WidgetsGallery/Demo/Box/Overview/React/Light/
import  {
  Box,
  Item
} from 'devextreme-react/box';

//import {
//  List
//} from 'devextreme-react/list';

//import {
//  apicall_promise,
//} from '../util.js';

import {
  api_version,
} from '../api.js';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

export default class Dashboard extends React.Component {
  _route () {
    return 'Dashboard';
  };

  componentDidMount () {
    setTimeout(function () {
      api_version(function (data) {
        this.setState({
          version: data.data
        })
      }.bind(this));
    }.bind(this), 500);
  };

  render () {
    if (!(this.state &&
          this.state.version)) {
      return null;
    }

    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>Dashboard</h1>

          <p>Version: {this.state.version.long}</p>

          <Foot { ...this.props } />
        </Item>

      </Box>
    );
  }
};
