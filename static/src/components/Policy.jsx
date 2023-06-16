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
import {UTPPolicy} from './UserTargetPolicy.jsx';

import 'devextreme-react/text-area';

export default class Policy extends SimpleResource {
  _route () {
    return 'Policy';
  };

  endpoint = 'policy';

  _onInitNewRow = function (ev) {
    if (this.props.hasOwnProperty('data')) {
      ev.data.policy_id = this.props.data.key;
    } else {
      ev.data.policy_id = null;
    }
  }.bind(this);

  _onRowInserting (ev) {
    ev.data.ts = null;
  }

  render () {
    const edopts_resizable = {
      autoResizeEnabled: true,
      elementAttr: {
        class: 'mn-code',
      },
    };

    return (
      <Box
        direction="row"
        width="100%"
      >
        <Item ratio={1}>
          <Head { ... this.props }  />

          <h1>Policy</h1>

          <DataGrid
            showBorders={false}
            dataSource={this._mnstore}

            onEditingStart={this._onEditingStart}
            onInitNewRow={this._onInitNewRow}
            onDataErrorOccurred={this._onDataErrorOccurred}
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
            </Column>

            <Column
              dataField="label"
              visible={true}
              allowEditing={true}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="statement"
              visible={true}
              allowEditing={true}
            >
              <RequiredRule />
            </Column>

            <Column
              dataField="ts"
              caption="Timestamp"
              dataType="datetime"
              visible={true}
              allowEditing={false}
            >
            </Column>

            <MasterDetail
              enabled={true}
              component={UTPPolicy}
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
                  <Item dataField="label" />
                  <Item
                    dataField="statement"
                    editorType="dxTextArea"
                    editorOptions={edopts_resizable}
                  />
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
