import hash from 'object-hash';

import {
  CACHE_DB_VERSION
} from './constant.js';

var _mncachedb = null;
const _mncachedbos = 'mncache';
const _mncache_expiration = 1000000000;

function _cleanup_mncachedb (db, cb) {
  const req = db.transaction(_mncachedbos, 'readwrite').objectStore(_mncachedbos).openCursor();
  req.onsuccess = function (ev) {
    const cursor = ev.target.result;

    if (cursor) {
      const mncitem = cursor.value;

      if ((mncitem.ts + _mncache_expiration) < Date.now()) {
        cursor.delete()
      };

      cursor.continue();
    }
    cb();
  };
};


function _init_mncachedb (req, cb) {
  const db = req.result;

  db.transaction(_mncachedbos)
        .objectStore(_mncachedbos).count().onsuccess = function (ev) {
    _mncachedb = db;
    _cleanup_mncachedb(db, cb);
  }
};


function _init_mncachedb_schema (ev) {
  const db = ev.target.result;

  //console.log(db);

  for (let i = 0; i < db.objectStoreNames.length; ++i) {
    db.deleteObjectStore(db.objectStoreNames[i]);
  }

  db.createObjectStore(_mncachedbos, {
    keyPath: 'id',
  });
};

export function setup_db (cb) {
  const req = window.indexedDB.open('cachdb', parseInt(CACHE_DB_VERSION));

  req.onerror = function (error) {
    console.error('mncachedb error:', error);
    //console.log('deleting db');
    window.indexedDB.deleteDatabase('mncachedb').onsuccess = (ev) => {
      //console.log('deleted mncachedb');
    };
  };

  req.onupgradeneeded = function (ev) {
    _init_mncachedb_schema(ev);
  };

  req.onsuccess = function (ev) {
    _init_mncachedb(req, cb);
  };
}

export function mncache_get (key, cb) {
  if (_mncachedb === null) {
    cb(null);

  } else {
    const os = _mncachedb.transaction(
      _mncachedbos).objectStore(_mncachedbos);

    const h = hash(key);

    os.get(h).onsuccess = function (ev) {
      const o = ev.target.result;

      if ((o === undefined) || ((o.ts + _mncache_expiration) < Date.now())) {
        cb(null);
      } else {
        cb(o);
      };
    };
  };
};


export function mncache_delete (key, cb) {
  if (_mncachedb === null) {
    cb(null);

  } else {
    const os = _mncachedb.transaction(
      _mncachedbos, 'readwrite').objectStore(_mncachedbos);

    const h = hash(key);

    os.delete(h).onsuccess = function (ev) {
      const o = ev.target.result;
      cb(o);
    };
  };
};


export function mncache_set_api_call (meth, what, params, udata, cb) {
  if (_mncachedb === null) {
    cb(udata);

  } else {
    const hinput = [meth, what, params];
    const h = hash(hinput);
    const mncitem = {
      id: h,
      value: udata,
      ts: Date.now(),
    };

    const os = _mncachedb.transaction(
      _mncachedbos, 'readwrite').objectStore(_mncachedbos);

    os.put(mncitem).onsuccess = function (ev) {
      cb(mncitem);
    };
  };
}

export function mncache_set (key, udata, cb) {
  if (_mncachedb === null) {
    cb(null);

  } else {
    const h = hash(key);
    const mncitem = {
      id: h,
      value: udata,
      ts: Date.now(),
    };

    const os = _mncachedb.transaction(
      _mncachedbos, 'readwrite').objectStore(_mncachedbos);

    os.put(mncitem).onsuccess = function (ev) {
      cb(mncitem);
    };
  };
}
