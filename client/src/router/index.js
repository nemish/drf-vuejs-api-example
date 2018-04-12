import Vue from 'vue';
import Router from 'vue-router';
import Shipments from '@/components/Shipments';
import Home from '@/components/Home';
import Auth from '@/components/Auth';
import Login from '@/components/Login';
import Register from '@/components/Register';
import ShipmentForm from '@/components/ShipmentForm';
import ShipmentsList from '@/components/ShipmentsList';

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
      {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
          {
            path: 'shipments',
            name: 'Shipments',
            component: Shipments,
            children: [{
                path: '',
                name: 'ShipmentsList',
                component: ShipmentsList
            }, {
                path: 'new',
                name: 'NewShipment',
                component: ShipmentForm
            }, {
                path: 'edit/:id',
                name: 'EditShipment',
                component: ShipmentForm
            }]
          },
          {
            path: 'auth',
            component: Auth,
            children: [{
                path: 'login',
                name: 'Login',
                component: Login
            },
            {
                path: 'register',
                name: 'Register',
                component: Register
            }]
          }
        ]
      },
      // { path: '*', redirect: '/' }
    ]
})
