import React from 'react';

import Toolbar, { Item } from 'devextreme-react/toolbar';

import {
  GUI_POLICY_TAG
} from '../constant.js';

import {
  parse_policy,
} from '../util.js';

export default class Head extends React.Component {
  render () {
    const policy = (this.props.uinfo !== null) ?
      parse_policy(this.props.uinfo.policy.statement) : {};

    const menu_items = policy.hasOwnProperty(GUI_POLICY_TAG) ?
      policy[GUI_POLICY_TAG][0].obj : null;

    return (
        <Toolbar>
        {
          Object.entries(this.props.routes).map(function ([key, value]) {
            const name = value[1];

            if ((name !== 'Logout') &&
                ((menu_items === null) ||
                  (!(menu_items.includes(name) ||
                     menu_items.includes('all'))))) {
              return null;
            }

            if ((name === 'Login') || (this.props.uinfo === null)) {
              return null;
            }

            const me_selected = window.location.pathname.indexOf(name) >= 0;

            const opts = {
              onClick: () => window.location.href = key,
              text: name,
              elementAttr: {
                class: me_selected ?
                  'mn-head-button-selected' : 'mn-head-button',
              },
            };

            return (
              <Item
                widget="dxButton"
                options={opts}
                key={key}
              />
            );
          }, this)
        }
        </Toolbar>
    );
  }
};
