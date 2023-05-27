import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import {
  DataGrid,
  Column,
  Sorting,
  Form,
  //FormItem,
  //Scrolling,
  HeaderFilter,
  Pager,
  Paging,
  Editing,
  SearchPanel,
  MasterDetail,
  //Lookup,
  RequiredRule,
} from 'devextreme-react/data-grid';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

import SimpleResource from './SimpleResource.jsx';
import {UTPUser} from './UserTargetPolicy.jsx';


export default class User extends SimpleResource {
  endpoint = 'user';

  _password_valid(row) {
    if (row.hasOwnProperty('password') || row.hasOwnProperty('password2')) {
      if (row.password !== row.password2) {
        throw new Error('password mismatch');
      }
    }
  };

  _onRowUpdating (ev) {
    //console.log('ORU', ev);
    try {
      this._password_valid(ev.newData)
    } catch (er) {
      ev.cancel = true;
      window.alert(`${er}`);
    };
  }

  _onRowInserting (ev) {
    ev.data.is_authenticated = true;
    ev.data.is_anonymous = false;

    try {
      this._password_valid(ev.data)
    } catch (er) {
      ev.cancel = true;
      window.alert(`${er}`);
    };
  }

  _onInitNewRow = function (ev) {
    if (this.props.hasOwnProperty('data')) {
      ev.data.user_id = this.props.data.key;
    } else {
      ev.data.user_id = null;
    }
  }.bind(this);

  render () {
    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>User</h1>

          <DataGrid
            showBorders={false}
            dataSource={this._mnstore}

            onEditingStart={this._onEditingStart}
            onInitNewRow={this._onInitNewRow}
            onDataErrorOccurred={this._onDataErrorOccurred}
            onRowUpdating={this._onRowUpdating.bind(this)}
            onRowInserting={this._onRowInserting.bind(this)}

            columnAutoWidth={false}
            columnMinWidth={100}
            focusedRowEnabled={true}

          >

            <SearchPanel
              visible={true}
              highlightCaseSensitive={true}
            />

            <HeaderFilter visible={true} allowSearch="true" />

            <Sorting mode="multiple" />

            <Column
              dataField="id"
              dataType="number"
              visible={true}
              allowEditing={false}
              width="10%"
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="login"
              visible={true}
              allowEditing={true}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="email"
              visible={true}
              allowEditing={true}
              editorOptions={{
                mode: 'email',
              }}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="password"
              visible={false}
              allowEditing={true}
              editorOptions={{
                mode: 'password',
              }}
            />
            <Column
              dataField="password2"
              caption="Password (again)"
              visible={false}
              allowEditing={true}
              editorOptions={{
                mode: 'password',
              }}
            />

            <Column
              dataField="apikey"
              visible={true}
              allowEditing={true}
            />

            <Column
              dataField="is_authenticated"
              dataType="boolean"
              visible={false}
              allowEditing={false}
            />

            <Column
              dataField="is_active"
              dataType="boolean"
              visible={true}
              allowEditing={true}
            >
            </Column>

            <Column
              dataField="is_anonymous"
              dataType="boolean"
              visible={false}
              allowEditing={false}
            />

            <MasterDetail
              enabled={true}
              component={UTPUser}
            />

            <Pager
              displayMode="full"
              allowedPageSizes={[25, 50, 100, 200]}
              showPageSizeSelector={true}
              showNavigationButtons={true}
              showInfo={true}
            />

            <Paging defaultPageSize={25} />

            <Editing
              mode="form"
              allowUpdating={true}
              allowDeleting={true}
              allowAdding={true}
            >
              <Form
                colCount="auto"
                labelMode="floating"
                labelLocation="top"
              >
                <Item itemType="group" colCount="1">
                  <Item dataField="login" />
                  <Item dataField="email" />
                </Item>

                <Item itemType="group" colCount="1">
                  <Item dataField="password" />
                  <Item dataField="password2" />
                  <Item dataField="apikey" />
                  <Item dataField="is_active" />
                </Item>

              </Form>
            </Editing>

          </DataGrid>

          <Foot { ...this.props } />
        </Item>

      </Box>
    );
  }
};
