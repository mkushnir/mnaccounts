import {
  apicall_promise,
} from './util.js';


function _api_call (method, what, params, data, cb) {
  try {
    apicall_promise(method, what, params, data).then(function (data) {
      cb(data);
    }).catch(function (error) {
      console.error(`${what} response error: ${error}`);
    });
  } catch (error) {
      console.error(`${what} api call error: ${error}`);
  };
}


export function api_version (cb) {
  _api_call('get', 'version', null, null, cb);
}
