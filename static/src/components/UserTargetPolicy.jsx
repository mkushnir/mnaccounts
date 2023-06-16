import React from 'react';

import  {
  Box,
  Item
} from 'devextreme-react/box';

import {
  DataGrid,
  Column,
  Sorting,
  //Form,
  //FormItem,
  //Scrolling,
  HeaderFilter,
  Pager,
  Paging,
  Editing,
  SearchPanel,
  //MasterDetail,
  Lookup,
  //RequiredRule,
} from 'devextreme-react/data-grid';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

import SimpleResource from './SimpleResource.jsx';
import User from './User.jsx';
import Target from './Target.jsx';
import Policy from './Policy.jsx';

export default class UserTargetPolicy extends SimpleResource {
  _route () {
    return 'UserTargetPolicy';
  };

  endpoint = 'user_target_policy';

  constructor (props) {
    super(props);

    this._user = new User({...props});
    this._target = new Target({...props});
    this._policy = new Policy({...props});
  };

  componentDidMount () {
    this._user._mnstore.load({}).then(function (data) {
      this.setState({
        user: data.data,
      });
    }.bind(this));

    this._target._mnstore.load().then(function (data) {
      this.setState({
        target: data.data,
      });
    }.bind(this));

    this._policy._mnstore.load().then(function (data) {
      this.setState({
        policy: data.data,
      });
    }.bind(this));

    this.setState({
      edit_user: false,
      edit_target: false,
    });
  }

  _onInitNewRow = function (ev) {
    if (this.props.hasOwnProperty('data') && (this.parent_endpoint !== null)) {
      const parent_id = `${this.parent_endpoint}_id`;
      ev.data[parent_id] = this.props.data.key;
    }

    this.setState({
      edit_user: true,
      edit_target: true,
    });
  }.bind(this);

  render () {
    if (!this.state.hasOwnProperty('user') ||
        !this.state.hasOwnProperty('target') ||
        !this.state.hasOwnProperty('policy') ||
        !this.state.hasOwnProperty('edit_user') ||
        !this.state.hasOwnProperty('edit_target')
    ) {
      return null;
    }

    const parent_id = `${this.parent_endpoint}_id`;

    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
      {
          (this.parent_endpoint === null) ? <Head { ... this.props }  /> : null
      }

      {
          (this.parent_endpoint === null) ?  <h1>User/Target/Policy Bindings</h1> : <h3>Bindings</h3>
      }



          <DataGrid
            showBorders={false}
            dataSource={this._mnstore}

            onEditingStart={this._onEditingStart}
            onInitNewRow={this._onInitNewRow}
            onDataErrorOccurred={this._onDataErrorOccurred}

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
              visible={false}
              allowEditing={false}
            >
      {
              //<RequiredRule />
      }
            </Column>

            <Column
              dataField="user_id"
              dataType="number"
              visible={('user_id' !== parent_id)}
              allowEditing={this.state.edit_user}
              caption='User'
            >
              <Lookup
                dataSource={this.state.user}
                valueExpr="id"
                displayExpr={(o) => (o !== null) ? `${o.login} (${o.email})` : ''}
              />
      {
              //<RequiredRule />
      }
            </Column>

            <Column
              dataField="target_id"
              dataType="number"
              visible={('target_id' !== parent_id)}
              allowEditing={this.state.edit_target}
              caption='Target'
            >
              <Lookup
                dataSource={this.state.target}
                valueExpr="id"
                displayExpr={(o) => (o !== null) ? `${o.label} (${o.url})` : ''}
              />
      {
              //<RequiredRule />
      }
            </Column>

            <Column
              dataField="policy_id"
              dataType="number"
              visible={('policy_id' !== parent_id)}
              allowEditing={true}
              caption='Policy'
            >
              <Lookup
                dataSource={this.state.policy}
                valueExpr="id"
                displayExpr="label"
              />
      {
              //<RequiredRule />
      }
            </Column>

            <Pager
              displayMode="full"
              allowedPageSizes={[25, 50, 100, 200]}
              showPageSizeSelector={true}
              showNavigationButtons={true}
              showInfo={true}
            />

            <Paging defaultPageSize={25} />

            <Editing
              mode="row"
              allowUpdating={true}
              allowDeleting={true}
              allowAdding={true}
            >
            </Editing>

          </DataGrid>

      {
        (this.parent_endpoint === null) ?  <Foot { ...this.props } /> : null
      }

        </Item>

      </Box>
    );
  }
};

export class UTPUser extends UserTargetPolicy {
  parent_endpoint = 'user';
};

export class UTPTarget extends UserTargetPolicy {
  parent_endpoint = 'target';
};

export class UTPPolicy extends UserTargetPolicy {
  parent_endpoint = 'policy';
};
