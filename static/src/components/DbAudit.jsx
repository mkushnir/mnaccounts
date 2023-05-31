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
  //Editing,
  SearchPanel,
  //MasterDetail,
  //Lookup,
  //RequiredRule,
} from 'devextreme-react/data-grid';

import Head from './Head.jsx';
import Foot from './Foot.jsx';

import SimpleResource from './SimpleResource.jsx';

import User from './User.jsx';

export default class DbAudit extends SimpleResource {
  endpoint = 'dbaudit';
  default_load_params = {
    sort: 'D'
  };

  constructor (props) {
    super(props);
    this._user = new User({...props});
  };

  componentDidMount () {
    this._user._mnstore.load({}).then(function (data) {
      this.setState({
        user: data.data,
      });
    }.bind(this));
  }

  _onInitNewRow = function (ev) {
    if (this.props.hasOwnProperty('data') && (this.parent_endpoint !== null)) {
      const parent_id = `${this.parent_endpoint}_id`;
      ev.data[parent_id] = this.props.data.key;
    }
  }.bind(this);

  render () {
    if (!this.state.hasOwnProperty('user')) {
      return null;
    }

    //const parent_id = `${this.parent_endpoint}_id`;

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
          (this.parent_endpoint === null) ?  <h1>DB Audit</h1> : <h3>DB Audit</h3>
      }



          <DataGrid
            showBorders={false}
            dataSource={this._mnstore}

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
            </Column>

            <Column
              dataField="dbts"
              caption="Timestamp"
              dataType="datetime"
              visible={true}
              allowEditing={false}
              width="7%"
            >
            </Column>

            <Column
              dataField="dbuser"
              caption="User"
              dataType="text"
              visible={true}
              allowEditing={false}
              width="7%"
            >
            </Column>

            <Column
              dataField="dbmethod"
              caption="Method"
              dataType="text"
              visible={true}
              allowEditing={false}
              width="7%"
            >
            </Column>

            <Column
              dataField="dbmodel"
              caption="Model"
              dataType="text"
              visible={true}
              allowEditing={false}
              width="7%"
            >
            </Column>

            <Column
              dataField="dbdata"
              dataType="object"
              caption="Data"
              customizeText={(o) => JSON.stringify(o['value'], null, 2)}
              visible={true}
              allowEditing={false}
            >
            </Column>

            <Pager
              displayMode="full"
              allowedPageSizes={[25, 50, 100, 200]}
              showPageSizeSelector={true}
              showNavigationButtons={true}
              showInfo={true}
            />

            <Paging defaultPageSize={25} />

          </DataGrid>

      {
        (this.parent_endpoint === null) ?  <Foot { ...this.props } /> : null
      }

        </Item>

      </Box>
    );
  }
};
