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
  RequiredRule,
} from 'devextreme-react/data-grid';

import SimpleResource from './SimpleResource.jsx';
import User from './User.jsx';
import Target from './Target.jsx';
import Policy from './Policy.jsx';

export default class UserTargetPolicy extends SimpleResource {
  endpoint = 'user_target_policy';

  constructor (props) {
    super(props);

    this._user = new User({...props});
    this._target = new Target({...props});
    this._policy = new Policy({...props});
  };

  render () {
    const parent_id = `${this.parent_endpoint}_id`;

    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
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
              visible={true}
              allowEditing={false}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="user_id"
              dataType="number"
              visible={('user_id' !== parent_id)}
              allowEditing={false}
            >
              <Lookup
                dataSource={this._user._mnstore}
                valueExpr="id"
                displayExpr={(o) => `${o.login} (${o.email})`}
              />
              <RequiredRule />
            </Column>

            <Column
              dataField="target_id"
              dataType="number"
              visible={('target_id' !== parent_id)}
              allowEditing={false}
            >
              <Lookup
                dataSource={this._target._mnstore}
                valueExpr="id"
                displayExpr={(o) => `${o.label} (${o.url})`}
              />
              <RequiredRule />
            </Column>

            <Column
              dataField="policy_id"
              dataType="number"
              visible={('policy_id' !== parent_id)}
              allowEditing={('policy_id' !== parent_id)}
            >
              <Lookup
                dataSource={this._policy._mnstore}
                valueExpr="id"
                displayExpr="label"
              />
              <RequiredRule />
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
