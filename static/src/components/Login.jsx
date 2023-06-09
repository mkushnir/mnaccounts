import React from 'react';

import {
  GUI_POLICY_TAG
} from '../constant.js';

import {
  logincall_promise,
} from '../util.js';

//import sprintf from 'sprintf-js';

import Form, {
  SimpleItem,
  EmptyItem,
  GroupItem,
  ButtonItem,
} from 'devextreme-react/form';


// https://js.devexpress.com/Demos/WidgetsGallery/Demo/Box/Overview/React/Light/
//import  {
//  Box,
//  Item
//} from 'devextreme-react/box';


import {
  mncache_set,
} from '../db.js';

import {
  parse_policy,
} from '../util.js';

import Head from './Head.jsx';

export default class Login extends React.Component {
  _route () {
    return 'Login';
  };

  constructor (props) {
    super(props);

    this.state = {
      data: {
        login: null,
        password: null,
        target: 'mna',
      },
    };
  };

  _do_login (ev) {
    //const params = {
    //  'mode': 'short',
    //};
    const params = null;
    logincall_promise (
      'POST',
      'account',
      params,
      this.state.data,
    ).then(function (data) {

      if (data === undefined) {
        //window.alert(sprintf.sprintf(formatMessage('mnLoginFailure'), user));
      } else {
        mncache_set('uinfo', data['data'], function (mncitem) {
          const policy = parse_policy(mncitem.value.policy.statement);

          const menu_items = policy.hasOwnProperty(GUI_POLICY_TAG) ?
            policy[GUI_POLICY_TAG][0].obj : null;

          if ((menu_items !== null) && (menu_items.length > 0)) {
            window.location.href = `/${menu_items[0]}`;
          }
        });

      }
    } /*.bind(this) */);
  };

  render () {
    return (
      <div>
        <Head { ... this.props }  />
        <React.Fragment>
          <Form
            colCount={3}
            formData={this.state.data}
          >
            <GroupItem
              colSpan={3}
              colCount={1}
            >
              <SimpleItem
                dataField="login"
              />

              <SimpleItem
                dataField="password"
                editorOptions={{
                  mode: 'password',
                }}
              />
            </GroupItem>
            
            <GroupItem
              colSpan={3}
              colCount={3}
            >
              <EmptyItem />
              <ButtonItem
                buttonOptions={{
                  text: 'Login',
                  onClick: this._do_login.bind(this),
                }}
              />
              <EmptyItem />
            </GroupItem>
          </Form>
        </React.Fragment>
      </div>
    );
  }
};
