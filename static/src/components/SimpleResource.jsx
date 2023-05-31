import React from 'react';

import CustomStore from 'devextreme/data/custom_store';

import {
  apicall_promise,
  //cmp_version,
} from '../util.js';

export default class SimpleResource extends React.Component {
  parent_endpoint = null;

  endpoint = null;
  default_load_params = {};

  _get_endpoint (meth) {
    return this.endpoint;
  }

  constructor (props) {
    super(props);

    this.state = {};

    this._onEditingStart = this._onEditingStart.bind(this);

    this._mnstore = new CustomStore({
      key: 'id',

      load: function (params) {
        let rparams = Object.assign(this.default_load_params);
        if (this.parent_endpoint !== null) {
          if (this.props.data && (this.props.data.column.command === 'detail')) {
            //rparams[sprintf.sprintf('%s.id', this.parent_endpoint)] = this.props.data.key;
            rparams[`${this.parent_endpoint}.id`] = this.props.data.key;

          } else if ((this.props.data.rowType && (this.props.data.rowType === 'detail'))) {
            //const parent_id_prop = sprintf.sprintf('%s_id', this.parent_endpoint);
            const parent_id_prop = `${this.parent_endpoint}_id`;

            if (this.props.data.data.hasOwnProperty(parent_id_prop)) {
              const parent_id = this.props.data.data[parent_id_prop];
              //rparams[sprintf.sprintf('%s.id', this.parent_endpoint)] = parent_id;
              rparams[`${this.parent_endpoint}.id`] = parent_id;
            }
          }
        }

        if (params.hasOwnProperty('hintfld')) {
          rparams.hintfld = params.hintfld;
          //rparams.sort = sprintf.sprintf('A:%s', params.hintfld);
          rparams.sort = `A:${params.hintfld}`;
        }

        if (params.hasOwnProperty('hintpfx')) {
          rparams.hintpfx = params.hintpfx;
        }

        if (params.hasOwnProperty('offset')) {
          rparams.offset = params.offset;
        }

        if (params.hasOwnProperty('limit')) {
          rparams.limit = params.limit;
        }

        const ep = this._get_endpoint('load');

        return apicall_promise('get', ep, rparams);
        //return apicall_promise_cached('get', ep, rparams);

      }.bind(this),

      byKey: function (key) {
        const ep = this._get_endpoint('byKey');
        //return apicall_promise('get', sprintf.sprintf('%s/%d', ep, key));
        return apicall_promise('get', `${ep}/${key}`);
        //return apicall_promise_cached('get', sprintf.sprintf('%s/%d', ep, key));

      }.bind(this),

      insert: function (data) {
        data.id = null;
        const ep = this._get_endpoint('insert');
        return apicall_promise('post', ep, null, data);
      }.bind(this),

      update: function (key, value) {
        if (key !== this.state.editing.id) {
          //throw Error(sprintf.sprintf(
          //  'error while editing: key %d !== id %d', key, this.editing.id));
          throw Error(`error while editing: key ${key} !== id ${this.editing.id}`);
        }

        const ep = this._get_endpoint('update');
        return apicall_promise(
          'put',
          //sprintf.sprintf('%s/%d', ep, key),
          `${ep}/${key}`,
          null,
          {...this.state.editing, ...value});

      }.bind(this),

      remove: function (key) {
        const ep = this._get_endpoint('remove');
        //return apicall_promise(
        //  'delete', sprintf.sprintf('%s/%d', ep, key));
        return apicall_promise('delete', `${ep}/${key}`);
      }.bind(this),
    });
  };

  // method not function, to allow override in subclasses (not final)
  _onEditingStart (ev) {
    this.setState({editing: ev.data});
  };
};
