const HOST = 'http://0.0.0.0:8001'

function makeQuery(payload) {
    const esc = encodeURIComponent;
    return Object.keys(payload || {})
        .map(k => `${esc(k)}=${esc(payload[k])}`)
        .join('&');
}

export const createFetchConf = (params) => {
    const { event, initialData, callbacks, dataProcessor } = params;
    const mutations = createFetchMutationsCallbacks(event, dataProcessor, callbacks);
    const { conf } = mutations;
    delete mutations.conf;
    return {
        state: {
            loading: false,
            data: initialData
        },
        mutations,
        conf
    };
}

export const createFetchMutationsCallbacks = (event, dataProcessor, callbacks) => {
    let conf = event;
    if (typeof event === 'string') {
        conf = createAsyncActionsConf(event);
    }
    return {
        [conf.startEvent](state, data) {
            state.loading = true;
        },
        [conf.successEvent](state, data) {
            if (dataProcessor) {
                data = dataProcessor(data);
            }
            Object.assign(state, {
                loading: false,
                data
            });
        },
        [conf.failEvent](state, action) {
            state.loading = false;
        },
        ...callbacks,
        conf
    }
}


export const createAsyncActionsConf = actionName => {
    return {
        actionName,
        startEvent: actionName + '__START',
        successEvent: actionName + '__SUCCESS',
        failEvent: actionName + '__FAIL',
    }
}


export function createFetchAction(conf) {
    const startEvent = `${conf.event}__START`;
    const successEvent = `${conf.event}__SUCCESS`;
    const failEvent = `${conf.event}__FAIL`;

    const fetchAction = ({commit, state, rootState, payload={}, actionPayload}) => {
      commit(startEvent, {
        ...payload,
        _actionPayload: actionPayload
      });
      let url = conf.url;
      let method = conf.method;
      if (typeof url === "function") {
        url = HOST + url(payload);
      } else {
        url = HOST + url;
      }

      if (typeof method === "function") {
        method = method(payload);
      }

      let params = {
          credentials: 'same-origin'
      };
      let headers = {};
      if (method === 'post' || method === 'put' || method === 'patch') {
        headers['Content-Type'] = 'application/json; charset=utf-8';
      }
      if (conf.authorized) {
        const { token } = rootState.user;
        if (token && token.length) {
            headers['Authorization'] = 'JWT ' + token;
        }
      }

      if (!method || method === 'get') {
        let query = makeQuery(payload);
        url = url + (query.length ? '?' + query : '');
      }

      if (method === 'post' || method === 'put' || method === 'patch') {
        params = {
            ...params,
            method: method.toUpperCase(),
            body: JSON.stringify(payload)
        }
      } else if (method === 'delete') {
        params = {
            method: 'DELETE'
        };
      }

      params.headers = headers;

      payload._actionPayload = actionPayload;

      return fetch(url, params)
        .then((resp) => {
            if (resp.ok) {
                return resp;
            }

            if (resp.status === 401) {
                localStorage.setItem('jwt_token', null);
            }

            return Promise.reject(resp);
        })
        .then(resp => {
            if (method === 'delete') {
                return {};
            }
            return resp.json()
        })
        .then(data => {
            if (data.errors && data.errors.length) {
                return Promise.reject(data);
            }
            if (actionPayload) {
                data._actionPayload = actionPayload;
            }
            commit(successEvent, data);
            return data;
        })
        .catch((err) => {
            commit(failEvent, payload);
            return Promise.reject(err);
        });
    };

    Object.assign(fetchAction, {
        startEvent,
        successEvent,
        failEvent,
        conf: createFetchConf(conf)
    });

    return fetchAction;
}

export default {
    createFetchAction
}