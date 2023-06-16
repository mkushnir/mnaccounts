import React from 'react';
import * as ReactDOM from 'react-dom/client';

import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

import './index.css';

import {
  setup_db,
  mncache_get,
} from './db.js';

import 'devextreme/dist/css/dx.material.blue.light.compact.css';
//import 'devextreme/dist/css/dx.material.blue.light.css';
//import 'devextreme/dist/css/dx.light.compact.css';
//import 'devextreme/dist/css/dx.light.css';

import Login from './components/Login.jsx';
import Dashboard from './components/Dashboard.jsx';
import User from './components/User.jsx';
import Target from './components/Target.jsx';
import Policy from './components/Policy.jsx';
import UserTargetPolicy from './components/UserTargetPolicy.jsx';
import DbAudit from './components/DbAudit.jsx';
import Manage from './components/Manage.jsx';
import Logout from './components/Logout.jsx';

class App extends React.Component {
  _all_components = [
    Login,
    Dashboard,
    User,
    Target,
    Policy,
    UserTargetPolicy,
    DbAudit,
    Manage,
    Logout,
  ];

  _component_name(component) {
    return component.prototype._route();
  }

  _build_path(name) {
    return `/${name}`;
  }

  constructor (props) {
    super(props);

    this._routes = {};
    this._all_components.forEach(function (component) {
      const name = this._component_name(component);
      this._routes[this._build_path(name)] = [component, name];
    }.bind(this));
    this.state = {
      uinfo: null,
      initialized: false,
    };
  };

  componentDidMount () {
    setup_db(function () {
      mncache_get('uinfo', function (mncitem) {
        this.setState({
          uinfo: (mncitem !== null) ? mncitem.value : null,
          initialized: true
        });
      }.bind(this));
    }.bind(this));
  };

  render () {
    //console.log('R', this.state);

    if (!this.state.initialized) {
      return null;
    }

    let r = this._routes[window.location.pathname];

    if (!r) {
      // default to Login
      const hr = this._build_path(
        this._component_name(this._all_components[0]));
      window.location.href = hr;

    } else {
      const component = r[0];
      const cname = this._component_name(component);

      if ((this.state.uinfo === null) && (cname !== 'Login')) {
        const hr = this._build_path(
          this._component_name(this._all_components[0]));
        window.location.href = hr;

      } else {
        const el = React.createElement(
          component,
          {
            components: this._all_components,
            routes: this._routes,
            uinfo: this.state.uinfo,
          }
        );

        return el;
      }
    }
  };
};


Sentry.init({
  dsn: 'https://c5735dcc92614d098be9592edb45a875@o764487.ingest.sentry.io/5794148',
  integrations: [new BrowserTracing()],
  tracesSampleRate: 1.0,
});


const root = ReactDOM.createRoot(document.getElementById('root'));


root.render(
    <App />
)
