import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import Form, {
  //GroupItem,
  SimpleItem,
  Label,
  ButtonItem,
  EmailRule,
} from 'devextreme-react/form';

import notify from 'devextreme/ui/notify';

import {
  api_user_put,
  api_usermanage,
} from '../api.js';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

export default class Manage extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      login: null,
      email: null,
      password: null,
      password2: null,
      is_active: null,
    };
  };

  _validate(row) {
    if (row.hasOwnProperty('password') || row.hasOwnProperty('password2')) {
      if (row.password !== row.password2) {
        throw new Error('password mismatch');
      }
    }

    if (!row.password) {
      delete row.password;
      delete row.password2;
    }
  };

  componentDidMount () {
    this.setState({ ...this.props.uinfo.user });
  };

  _button_clicked (ev) {
    if (this.state.is_active) {
      try {
        const data = {
          id: this.state.id,
          login: this.state.login,
          email: this.state.email,
          password: this.state.password,
          password2: this.state.password2,
          is_active: this.state.is_active,
          is_authenticated: this.state.is_authenticated,
          is_anonymous: this.state.is_anonymous,
        };

        this._validate(data);

        api_user_put(this.state.id, data, function (rv) {
          notify('Updated OK, logging out ...');
          setTimeout(() => {
            window.location.href = '/Logout';
          }, 1500);
        });

      } catch (er) {
        ev.cancel = true;
        window.alert(`${er}`);
      };
    } else {
      const p = {
        id: null,
        operation: 'set-active',
          params: {
            flag: false,
          },
      };

      api_usermanage(this.state.id, p, function (data) {
        notify('De-activated OK, logging out ...');
        setTimeout(() => {
          window.location.href = '/Logout';
        }, 1500);
      });
    }
  };

  _form_initialized (ev) {
    this.form = ev.component;

    const bo = {
      text: 'Update',
      type: 'default',
      width: '10vw',
      onClick: this._button_clicked.bind(this),
    };

    this.form.itemOption('submit_button', 'buttonOptions', bo);
  };

  _is_active_changed (ev) {
    if (!ev.value) {
      this.setState({
        ...this.props.uinfo.user,
        password: null,
        password2: null,
        is_active: ev.value,
      });
    }

    const eo = {'disabled': !ev.value};

    this.form.itemOption('email', 'editorOptions', eo);
    this.form.itemOption('password', 'editorOptions', eo);
    this.form.itemOption('password2', 'editorOptions', eo);
    this.form.itemOption('password2', 'editorOptions', eo);

    const o = this.form.itemOption('submit_button')
    o.buttonOptions.type = ev.value ? 'default' : 'danger';
    o.buttonOptions.text = ev.value ? 'Update' : 'Suspend';
    this.form.itemOption('submit_button', 'buttonOptions', o.buttonOptions);
  }

  render () {
    if (!this.state.hasOwnProperty('login')) {
      return null;
    }

    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>Manage</h1>

          <Form
      activeStateEnabled={true}
            colCount={2}
            formData={this.state}
      onInitialized={this._form_initialized.bind(this)}
          >
            <SimpleItem
              dataField="login"
              editorType="dxTextBox"
      editorOptions={{
        disabled: true,
      }}
            >
              <Label text="Login" />
            </SimpleItem>

            <SimpleItem
              dataField="email"
              editorType="dxTextBox"
              editorOptions={{
                mode: 'email',
              }}
            >
              <Label text="Set E-mail" />
              <EmailRule />
            </SimpleItem>

            <SimpleItem
              dataField="password"
              editorType="dxTextBox"
              editorOptions={{
                mode: 'password',
              }}
            >
              <Label text="Set Password" />
            </SimpleItem>

            <SimpleItem
              dataField="password2"
              editorType="dxTextBox"
              editorOptions={{
                mode: 'password',
              }}
            >
              <Label text="Repeat Password" />
            </SimpleItem>

            <SimpleItem
              dataField="is_active"
              editorType="dxCheckBox"
      editorOptions={{
        onValueChanged: this._is_active_changed.bind(this)
      }}
            >
              <Label text="Active" />
            </SimpleItem>

            <ButtonItem
  name="submit_button"
      hotizontalAlignment="center"
            />

          </Form>

          <Foot { ...this.props } />
        </Item>

      </Box>
    );
  }
};
