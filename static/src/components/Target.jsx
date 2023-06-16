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
  MasterDetail,
  //Lookup,
  RequiredRule,
} from 'devextreme-react/data-grid';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

import SimpleResource from './SimpleResource.jsx';
import {UTPTarget} from './UserTargetPolicy.jsx';


export default class Target extends SimpleResource {
  _route () {
    return 'Target';
  };

  endpoint = 'target';

  _onInitNewRow = function (ev) {
    if (this.props.hasOwnProperty('data')) {
      ev.data.target_id = this.props.data.key;
    } else {
      ev.data.target_id = null;
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

          <h1>Target</h1>

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
              width="10%"
            >
            </Column>

            <Column
              dataField="label"
              visible={true}
              allowEditing={true}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="url"
              visible={true}
              allowEditing={true}
              editorOptions={{
                mode: 'url',
              }}
            >
              <RequiredRule />
            </Column>

            <MasterDetail
              enabled={true}
              component={UTPTarget}
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
              mode="row"
              allowUpdating={true}
              allowDeleting={true}
              allowAdding={true}
            >
            </Editing>

          </DataGrid>

          <Foot { ...this.props } />
        </Item>

      </Box>
    );
  }
};
