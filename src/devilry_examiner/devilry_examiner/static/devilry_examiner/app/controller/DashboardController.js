// Generated by CoffeeScript 1.6.3
(function() {
  Ext.define('devilry_examiner.controller.DashboardController', {
    extend: 'Ext.app.Controller',
    views: ['dashboard.YourAssignments'],
    stores: [],
    models: ['YourAssignments'],
    refs: [
      {
        ref: 'yourAssignments',
        selector: 'yourAssignments'
      }
    ],
    init: function() {
      return this.control({
        'yourAssignments': {
          render: this._onRenderYourAssignments
        }
      });
    },
    _onRenderYourAssignments: function() {
      console.log(this.getYourAssignmentsModel());
      return this.getYourAssignments().update({
        assignments: [
          {
            long_name: 'Oblig 1'
          }, {
            long_name: 'Oblig 2'
          }
        ]
      });
    }
  });

}).call(this);
