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
              login: {window.localStorage.getItem('login')}
              <br/>
              e-mail: {window.localStorage.getItem('email')}
            </small>
          </p>
        </Item>
      </Box>
    );
  }
};
