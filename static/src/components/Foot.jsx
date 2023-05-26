import React from 'react';

// https://js.devexpress.com/Demos/WidgetsGallery/Demo/Box/Overview/React/Light/
import  {
  Box,
  Item
} from 'devextreme-react/box';


export default class Foot extends React.Component {

  render () {
    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <p className="mn-dashboard-user">
            <small>
              login: {this.props.uinfo.user.login}
              <br/>
              e-mail: {this.props.uinfo.user.email}
            </small>
          </p>
        </Item>
      </Box>
    );
  }
};
