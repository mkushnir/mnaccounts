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


// api
export function api_version (cb) {
  _api_call('get', 'version', null, null, cb);
}

export function api_usermanage (user_id, data, cb) {
  _api_call('put', `user/manage/${user_id}`, null, data, cb);
}

export function api_user_put (user_id, data, cb) {
  _api_call('put', `user/${user_id}`, null, data, cb);
}
