import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import {
  logincall_promise,
} from '../util.js';

import {
  mncache_delete,
} from '../db.js';

import Head from './Head.jsx';

export default class Logout extends React.Component {
  _route () {
    return 'Logout';
  };


  constructor (props) {
    super(props);
    window.localStorage.clear();
  };

  componentDidMount () {
    if (this.props.uinfo !== null) {
      logincall_promise (
        'DELETE',
        'account',
        null,
        {
          ticket: this.props.uinfo.ticket.ticket,
        }
      ).then(function (data) {
        // pass
      });
    };

    mncache_delete('uinfo', function (o) {
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
