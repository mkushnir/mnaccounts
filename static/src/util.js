import sprintf from 'sprintf-js';
//import hash from 'object-hash';

import {
  formatMessage,
} from 'devextreme/localization';


import {
  APIHOST,
  LOGINHOST,
  GUI_POLICY_TAG
} from  './constant.js'

const re_cookie = new RegExp('^([^=]+)=(.*)$');


export function parse_cookie (cookie, honor_clear) {
  const decoded = decodeURIComponent(cookie);
  const pieces = decoded.split(';');

  const cook = Object();

  for (let i = 0; i < pieces.length; ++i) {
    const m = pieces[i].match(re_cookie);

    if (m !== null) {
      const k = m[1].trim();
      const v = m[2];
      if (cook.hasOwnProperty(k)) {
        if (honor_clear) {
          if (cook[k] === '') {
            continue;
          } else if (v === '') {
            cook[k] = v;
          }
        }
      } else {
        cook[k] = m[2];
      }
    }
  }

  return cook;
}

export function build_loginurl (what, params=null) {
  const url = new URL(what, LOGINHOST);

  var qstr = '';
  if (params) {
    let pieces = [];
    for (const [k, v] of Object.entries(params)) {
      if (Array.isArray(v)) {
        for (const i of v) {
          pieces.push(sprintf.sprintf(
            '%s=%s', encodeURIComponent(k), encodeURIComponent(i)));
        }
      } else {
        // scalars expected
        pieces.push(sprintf.sprintf(
          '%s=%s', encodeURIComponent(k), encodeURIComponent(v)));
      }
    }
    qstr = '?' + pieces.join('&');
  }
  url.search = qstr;
  return url;

  //console.log(url);

  //return sprintf.sprintf('%s%s%s', LOGINHOST, what, qstr);
}


export function logincall_promise (meth, what, params=null, data=null) {
  let fparams = {
    method: meth,
    credentials: 'include',
    mode: 'cors',
  };

  if (data !== null) {
    fparams.body = JSON.stringify(data);
    fparams.headers = {
      'Content-Type': 'application/json',
    };
  }

  const url = build_loginurl(what, params);

  return fetch(url, fparams).then(function (response) {
    //console.log('LCP', response.headers.get('Set-Cookie'));

    if (!response.ok) {
      response.text().then(function (s) {
        //console.log('s', s);

        const m = JSON.parse(s);

        const msg = m.hasOwnProperty('msg') ? m.msg : JSON.stringify(m.message);
        const args = m.hasOwnProperty('args') ? m.args : [];

        const fmsg0 = formatMessage(msg);
        const fmsg1 = sprintf.sprintf(fmsg0 ? fmsg0 : msg, ...args);

        window.alert(sprintf.sprintf(
          'Login error.\nStatus: %d\nMessage: %s',
          response.status,
          fmsg1 ? fmsg1 : msg));

      }).catch(function (error) {
        console.error('logincall_promise response body error', error);
      });
    }

    return response.json();

  }).catch(function (error) {
    console.error('logincall_promise fetch error', error);
  })
};


export function build_apiurl (what, params=null) {
  var qstr = '';
  if (params) {
    let pieces = [];
    for (const [k, v] of Object.entries(params)) {
      if (Array.isArray(v)) {
        for (const i of v) {
          pieces.push(sprintf.sprintf(
            '%s=%s', encodeURIComponent(k), encodeURIComponent(i)));
        }
      } else {
        // scalars expected
        pieces.push(sprintf.sprintf(
          '%s=%s', encodeURIComponent(k), encodeURIComponent(v)));
      }
    }
    qstr = '?' + pieces.join('&');
  }

  return sprintf.sprintf('%s%s%s', APIHOST, what, qstr);
}


export function apicall (meth, what, params, data, hdata, herror) {
  const fparams = {
    method: meth,
    body: (data !== null) ? (JSON.stringify(data)) : null,
    credentials: 'include',
  };

  fetch(
    build_apiurl(what, params),
    fparams
  ).then(
    function (response) {
      return response.json();
    }
  ).then(
    function (data) {
      hdata(data);
    },
    function (error) {
      herror(error);
    }
  );
}


export function apicall_promise (meth, what, params=null, data=null, cb=null) {
  let fparams = {
    method: meth,
    headers: {},
    credentials: 'include',
  };

  //const access_token = window.localStorage.getItem('access_token');
  //const apikey = window.localStorage.getItem('apikey');
  //const login = window.localStorage.getItem('login');
  //const password = window.localStorage.getItem('password');

  //if (access_token) {
  //  fparams.headers['Authorization'] = sprintf.sprintf(
  //    'Bearer %s', access_token);

  //} else if (apikey) {
  //  fparams.headers['Authorization'] = sprintf.sprintf(
  //    'apikey %s', apikey);

  //} else if (login && password) {
  //  fparams.headers['Authorization'] = sprintf.sprintf(
  //    'Basic %s', btoa(sprintf.sprintf('%s:%s', login, password)));
  //}

  //if (!fparams.headers.hasOwnProperty('Authorization')) {
  //  throw Error(`API Not Logged In when calling ${meth} ${what} ${params}`);
  //}

  if (data !== null) {
    fparams.body = JSON.stringify(data);
    fparams.headers['Content-Type'] = 'application/json';
  }

  //console.log(fparams);

  const url = build_apiurl(what, params);

  return fetch(url, fparams).then(function (response) {
    if (!response.ok) {
      response.text().then(function (s) {
        const m = JSON.parse(s);

        const msg = m.hasOwnProperty('msg') ? m.msg : JSON.stringify(m.message);
        const args = m.hasOwnProperty('args') ? m.args : [];

        const fmsg0 = formatMessage(msg);
        const fmsg1 = sprintf.sprintf(fmsg0 ? fmsg0 : msg, ...args);

        window.alert(sprintf.sprintf(
          'API error.\nStatus: %d\nMessage: %s',
          response.status,
          fmsg1 ? fmsg1 : msg));

      }).catch(function (error) {
        console.error('apicall_promise response body error', error);
      });

      const p = new Promise(function (resolve, reject) {
        resolve(null);
      });

      if (cb === null) {
        return p;
      } else {
        return cb(p);
      }
    } else {
      if (cb === null) {
        return response.json();
      } else {
        return cb(response.json());
      }
    }

  }).catch(function (error) {
    console.error('apicall_promise fetch error', error);
  });
};


export function setup_loggedin_status (cb) {
  logincall_promise (
    'GET',
    'session',
    null,
    null,
  ).then(function (data) {
    cb(data);
  }).catch(function (error) {
    console.error('setup_loggedin_status: response body error', error);
  });
}


export function cmpa (a, b) {
  let res = 0;
  const len = Math.max(a.length, b.length);
  for (let i = 0; i < len; ++i) {
    if (a[i] < b[i] || (a[i] === undefined)) {
      res = -1;
      break;
    } else if (a[i] > b[i] || (b[i] === undefined)) {
      res = 1;
      break;
    }
  }
  return res;
};


const _re_alnum = new RegExp('(^|[/,.:;-]+)([^/,.:;-]+)', 'g');


export function cmp_version (va, vb) {
  const _f = function (i) {
    const n = parseInt(i[2]);
    if (isNaN(n)) {
      return i[2];
    } else {
      return n;
    }
  };

  //console.log(va);
  //console.log(vb);

  if (va === null) {
    if (vb === null) {
      return 0;
    } else {
      return 1;
    }
  } else {
    if (vb === null) {
      return 1;
    }
  }

  //console.log('va', va);
  //console.log('vb', vb);

  const a = Array.from(va.matchAll(_re_alnum), _f);
  const b = Array.from(vb.matchAll(_re_alnum), _f);

  return cmpa(a, b);
};


const _re_policy_statement = new RegExp('\\s*(\\S+)\\s+(.+?)\\s+(\\baccept|\\breject|\\bnull)?\\s*;', 'gs');
const _policy_tags = [GUI_POLICY_TAG];

export function parse_policy (stmt) {
  const m = stmt.matchAll(_re_policy_statement);

  const a = Array.from(m, function (i) {
    const st = {
      tag: i[1],
      expr: i[2],
      action: i[3],
    };
    return st;
  });

  const res = {};

  a.filter(function (i) {
    return _policy_tags.includes(i.tag);
  }).forEach(function (i) {
    if (!res.hasOwnProperty(i.tag)) {
      res[i.tag] = [];
    }

    res[i.tag].push({
      obj: JSON.parse(i['expr']), // "obj" is a parsed "expr"
      ...i,
    });
  });

  return res;
}
