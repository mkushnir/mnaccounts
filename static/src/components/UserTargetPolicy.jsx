import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

export default class UserTargetPolicy extends React.Component {
  render () {
    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>UserTargetPolicy</h1>

          <Foot />
        </Item>

      </Box>
    );
  }
};
