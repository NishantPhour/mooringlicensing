import Vue from 'vue'
import resource from 'vue-resource'
import App from './App'
import router from './router'
import bs from 'bootstrap'
import helpers from '@/utils/helpers'

import { extendMoment } from 'moment-range';

import 'datatables.net';
import 'datatables.net-bs';
import 'datatables.net-buttons-bs';
import 'datatables.net-responsive-bs';
import 'datatables.net-buttons/js/dataTables.buttons.js';
import 'datatables.net-buttons/js/buttons.html5.js';

import jszip from 'jszip';
window.JSZip = jszip;

import "datatables.net-bs/css/dataTables.bootstrap.css";
import "datatables.net-responsive-bs/css/responsive.bootstrap.css";

import 'select2';
import 'jquery-validation';

import "sweetalert2/dist/sweetalert2.css";
import 'select2/dist/css/select2.min.css';
import 'select2-bootstrap-theme/dist/select2-bootstrap.min.css';
import '@/../node_modules/datatables.net-bs/css/dataTables.bootstrap.min.css';
import '@/../node_modules/datatables.net-responsive-bs/css/responsive.bootstrap.min.css';


extendMoment(moment);

import api_endpoints from './api'
require('../node_modules/bootstrap/dist/css/bootstrap.css' );
require('../node_modules/eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css')
require('../node_modules/font-awesome/css/font-awesome.min.css' )

Vue.config.devtools = true;
Vue.config.productionTip = false
Vue.use( resource );

// Add CSRF Token to every request
Vue.http.interceptors.push( function ( request, next ) {
  // modify headers
  if ( request.url != api_endpoints.countries ) {
    request.headers.set( 'X-CSRFToken', helpers.getCookie( 'csrftoken' ) );
  }

  // continue to next interceptor
  next();
} );


/* eslint-disable no-new */
new Vue( {
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
} )
