odoo.define('bsc.bsc_dashboard', function (require) {
    "use strict"
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    
    var _t = core._t;
    var QWeb = core.qweb;

    
    var BscDashboard = Widget.extend({
        className: 'mail_client_home_page',
        // template: "BscDashboardTemplate",
        start: function(){
            var self = this;
            var Bsc = new Model('bsc.dashboard');

            Bsc.call('get_bsc_data',
            [
                ['/'],
                []
            ],
            {})
            .then (function (list) {
                console.log(list)
                console.log(list[0].objectives)
                self.$el.append(QWeb.render('BscDashboardTemplate', {'list': list}));
            });
        },
        });
    core.action_registry.add('bsc_dashboard', BscDashboard);

    return BscDashboard;
});
