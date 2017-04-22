'use strict';


var alertaApp = angular.module('alertaApp', [
  'config',
  'ngRoute',
  'ngSanitize',
  'alertaFilters',
  'alertaServices',
  'alertaDirectives',
  'alertaControllers',
  'satellizer'
])

alertaApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider
    .when('/pages/alerta/', {
      templateUrl: 'pages/alerta/alert-list.html',
      controller: 'AlertListController',
      reloadOnSearch: false
    })
    .when('/alert/:id', {
      templateUrl: 'pages/alerta/alert-details.html',
      controller: 'AlertDetailController'
    })
    .when('/top10', {
      templateUrl: 'pages/alerta/alert-top10.html',
      controller: 'AlertTop10Controller',
      reloadOnSearch: false
    })
    .when('/watch', {
      templateUrl: 'pages/alerta/alert-watch.html',
      controller: 'AlertWatchController'
    })
    .when('/blackouts', {
      templateUrl: 'pages/alerta/blackouts.html',
      controller: 'AlertBlackoutController'
    })
    .when('/users', {
      templateUrl: 'pages/alerta/users.html',
      controller: 'UserController'
    })
    .when('/customers', {
      templateUrl: 'pages/alerta/customers.html',
      controller: 'CustomerController'
    })
    .when('/keys', {
      templateUrl: 'pages/alerta/keys.html',
      controller: 'ApiKeyController'
    })
    .when('/profile', {
      templateUrl: 'pages/alerta/profile.html',
      controller: 'ProfileController'
    })
    .when('/heartbeats', {
      templateUrl: 'pages/alerta/heartbeats.html',
      controller: 'HeartbeatsController'
    })
    .when('/about', {
      templateUrl: 'pages/alerta/about.html',
      controller: 'AboutController'
    })
    .when('/login', {
      templateUrl: 'pages/alerta/login.html',
      controller: 'LoginController'
    })
    .when('/signup', {
      templateUrl: 'pages/alerta/signup.html',
      controller: 'SignupController'
    })
    .when('/logout', {
      templateUrl: 'pages/alerta/logout.html',
      controller: 'LogoutController'
    })
    .otherwise({
      redirectTo: '/pages/alerta/'
    });
  }]);

alertaApp.config(['$httpProvider',
  function ($httpProvider) {
    $httpProvider.interceptors.push(function ($q, $location) {
        return {
            'response': function (response) {
                //Will only be called for HTTP up to 300
                return response;
            },
            'responseError': function (rejection) {
                if(rejection.status === 401) {
                    $location.path('/login');
                }
                return $q.reject(rejection);
            }
        };
    });
}]);

alertaApp.config(['config', '$authProvider',
  function (config, $authProvider) {
    $authProvider.loginUrl = config.endpoint+'/auth/login';
    $authProvider.signupUrl = config.endpoint+'/auth/signup';
    $authProvider.logoutRedirect = '/login';
    $authProvider.google({
      url: config.endpoint+'/auth/google',
      clientId: config.client_id
    });
    $authProvider.github({
      url: config.endpoint+'/auth/github',
      clientId: config.client_id,
      scope: ['user:email', 'read:org'],
      authorizationEndpoint: (config.github_url || 'https://github.com')+'/login/oauth/authorize'
    });
    $authProvider.oauth2({
      name: 'gitlab',
      url: config.endpoint+'/auth/gitlab',
      redirectUri: window.location.origin,
      clientId: config.client_id,
      authorizationEndpoint: config.gitlab_url+'/oauth/authorize'
    });
    $authProvider.oauth2({
      name: 'keycloak',
      url: config.endpoint+'/auth/keycloak',
      redirectUri: window.location.origin,
      clientId: config.client_id,
      authorizationEndpoint: config.keycloak_url+'/auth/realms/'+config.keycloak_realm+'/protocol/openid-connect/auth'
    });
}]);
