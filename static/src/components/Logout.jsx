import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import {
  mncache_delete,
} from '../db.js';

import Head from './Head.jsx';

export default class Logout extends React.Component {
  constructor (props) {
    super(props);
    window.localStorage.clear();
  };

  componentDidMount () {
    mncache_delete('uinfo', function (o) {
      //console.log('uinfo:', o);
      setTimeout(function () {
        window.location.href = '/Login';
      }, 2500);
    });
  };

  render () {
    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>Logout</h1>

          <p>Please wait until you are logged out ...</p>

        </Item>

      </Box>
    );
  }
};
