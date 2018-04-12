import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from 'vuex/dist/logger';

import {
    createFetchAction,
    createAsyncActionsConf,
    createFetchConf
} from '../utils/actions';

const SET_USER_TOKEN = 'SET_USER_TOKEN';
const FECTH_CURRENT_USER = 'FECTH_CURRENT_USER';
const FECTH_SHIPMENTS = 'FECTH_SHIPMENTS';
const LOGIN = 'LOGIN';
const VERIFY_TOKEN = 'VERIFY_TOKEN';
const LOGOUT = 'LOGOUT';
const REGISTER = 'REGISTER';
const CREATE_SHIPMENT = 'CREATE_SHIPMENT';
const UPDATE_SHIPMENT = 'UPDATE_SHIPMENT';
const DELETE_SHIPMENT = 'DELETE_SHIPMENT';

const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj));
}

const fetchShipmentsList = createFetchAction({
    url: '/shipments/',
    authorized: true,
    event: FECTH_SHIPMENTS,
});

const fetchCurrentUser = createFetchAction({
    url: '/get_user',
    authorized: true,
    event: FECTH_CURRENT_USER
});

const login = createFetchAction({
    url: '/auth/token/obtain/',
    event: LOGIN,
    method: 'post'
});

const verifyToken = createFetchAction({
    url: '/auth/token/verify/',
    event: VERIFY_TOKEN,
    method: 'post'
});

const createShipment = createFetchAction({
    url: '/shipments/',
    event: CREATE_SHIPMENT,
    authorized: true,
    method: 'post'
});

const deleteShipment = createFetchAction({
    url: (item) => `/shipments/${item.id}/`,
    event: DELETE_SHIPMENT,
    authorized: true,
    method: 'delete'
});

const updateShipment = createFetchAction({
    url: (payload) => `/shipments/${payload.id}/`,
    event: UPDATE_SHIPMENT,
    authorized: true,
    method: 'patch'
});

const register = createFetchAction({
    url: '/register',
    event: REGISTER,
    method: 'post'
});

const logout = createFetchAction({
    url: '/logout',
    event: LOGOUT,
    method: 'post'
});


const handleFetchUser = ({commit, state, rootState}) => {
    const token = localStorage.getItem('jwt_token');
    if (!state.token && token) {
        commit(SET_USER_TOKEN, { token });
        return verifyToken({commit, state, rootState, payload: { token }});
    }
    return Promise.reject();
}


Vue.use(Vuex);

const INITIAL_REMOTE_SINGLE_OBJ_STATE = {
    loading: false,
    data: {}
};

const INITIAL_REMOTE_LIST_OBJECTS_STATE = {
    loading: false,
    data: []
};


const createFormModule = (conf = {}) => {
    return {
        namespaced: true,
        state: {
            _meta: {
                errors: []
            }
        },
        actions: {
            loadSelect({commit, state, dispatch, rootState}, actionPayload) {
                const {url} = actionPayload;
                return createFetchAction({
                    url,
                    event: `LOAD_OPTIONS`,
                    authorized: true
                })({state, commit, rootState, actionPayload});
            },
            changeValue({commit, state, dispatch}, data) {
                commit('changeValue', data);
                if (conf.changeCb) {
                    conf.changeCb({commit, dispatch, state, data});
                }
            },
            initFormValues({commit, state, dispatch}, data) {
                commit('initFormValues', data);
            },
            ...conf.actions
        },
        mutations: {
            changeValue(state, {name, value}) {
                Vue.set(state, name, value);
            },
            initFormValues(state, data) {
                Object.keys(data).forEach(key => {
                    state[key] = data[key];
                });
            },
            LOAD_OPTIONS__START(state, payload) {
                const {name} = payload._actionPayload;
                Vue.set(state._meta, name, {
                    loading: true
                });
            },
            LOAD_OPTIONS__FAIL(state, payload) {
                const {name} = payload._actionPayload;
                Vue.set(state._meta, name, {
                    loading: false
                });
            },
            LOAD_OPTIONS__SUCCESS(state, data) {
                const {name} = data._actionPayload;
                Vue.set(state._meta, name, {
                    loading: false,
                    options: data
                });
            },
            ...conf.mutations
        }
    };
}


const shipmentFormActions = [
    createShipment,
    updateShipment
];


export const store = new Vuex.Store({
    plugins: [createLogger()],
    modules: {
        loginForm: createFormModule({
            changeCb({commit}) {
                commit('user/resetErrors', null, {root: true})
            }
        }),
        shipmentForm: createFormModule({
            changeCb({commit}) {
                commit('resetErrors');
            },
            actions: {
                createShipment({ commit, state, rootState }, payload) {
                    return createShipment({ commit, state, rootState, payload})
                },
                updateShipment({ commit, state, rootState }, payload) {
                    return updateShipment({ commit, state, rootState, payload})
                }
            },
            mutations: Object.assign.apply({}, shipmentFormActions.map(action => {
                return {
                    [action.startEvent](state) {
                        state._meta.loading = true;
                    },
                    [action.successEvent](state, data) {
                        Object.keys(state).forEach(key => {
                            if (key === '_meta') {
                                return;
                            }
                            state[key] = null;
                        })
                        state._meta.loading = false;
                    },
                    [action.failEvent](state, data) {
                        state._meta.loading = false;
                        state._meta.errors = ['Check form for errors and try again'];
                    },
                    resetErrors(state) {
                        state._meta.errors = [];
                    }
                }
            }))
        }),
        shipments: {
            namespaced: true,
            state: {
                ...INITIAL_REMOTE_LIST_OBJECTS_STATE,
                pager: {},
                total: 0
            },
            actions: {
                fetchList({ commit, state, rootState }, payload) {
                    return fetchShipmentsList({commit, state, rootState, payload});
                },
                deleteShipment({ commit, state, rootState }, payload) {
                    return deleteShipment({commit, state, rootState, payload});
                }
            },
            mutations: {
                [fetchShipmentsList.startEvent](state) {
                    state.loading = true;
                },
                [fetchShipmentsList.successEvent](state, data) {
                    Object.assign(state, { data: data.results, pager: data.pager, total: data.count });
                    state.loading = false;
                },
                [fetchShipmentsList.failEvent](state, data) {
                    state.loading = false;
                },
                [deleteShipment.startEvent](state) {
                    state.loading = true;
                },
                [deleteShipment.failEvent](state, data) {
                    state.loading = false;
                }
            },
        },
        user: {
            namespaced: true,
            state: {
                ...INITIAL_REMOTE_SINGLE_OBJ_STATE,
                errors: []
            },
            getters: {
                loggedIn: state => !!state.data.id
            },
            actions: {
                fetchCurrentUser(context) {
                    return handleFetchUser(context);
                },
                login({ commit, state, rootState }, payload) {
                    return login({commit, state, rootState, payload}).then(data => {
                        commit(SET_USER_TOKEN, data);
                    });
                },
                logout({ commit, state }, data) {
                    commit(SET_USER_TOKEN, {token: null});
                    commit('reset');
                },
            },
            mutations: {
                [SET_USER_TOKEN](state, data) {
                    const { token } = data;
                    localStorage.setItem('jwt_token', token);
                    state.token = token;
                },
                reset(state, data) {
                    Object.assign(state, INITIAL_REMOTE_SINGLE_OBJ_STATE);
                },
                [login.startEvent](state) {
                    state.loading = true;
                },
                [verifyToken.startEvent](state) {
                    state.loading = true;
                },
                [login.successEvent](state, data) {
                    Object.assign(state, {data: data.user});
                    state.loading = false;
                },
                [verifyToken.successEvent](state, data) {
                    Object.assign(state, {data: data.user});
                    state.loading = false;
                },
                [verifyToken.failEvent](state, data) {
                    state.token = null;
                    state.loading = false;
                },
                [login.failEvent](state, data) {
                    state.token = null;
                    state.loading = false;
                    state.errors = ['Error. Please, check credentials'];
                },
                resetErrors(state) {
                    state.errors = [];
                }
            },
        },
    },
});

export default {
    store,
};