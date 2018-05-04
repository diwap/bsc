odoo.define('bsc.bsc_dashboard', function (require) {
    "use strict";
    var core = require('web.core');
    var rpc = require('web.rpc');
    var Widget = require('web.Widget');
    
    var _t = core._t;
    var QWeb = core.qweb;

    
    var BscDashboard = Widget.extend({
        className: 'mail_client_home_page',
        // template: "BscDashboardTemplate",
        start: function(){
            var self = this;
            rpc.query({
                model: 'bsc.dashboard',
                method: 'get_bsc_data',
                args: [],
            }).then((res) => {
                console.log(res)
                self.$el.append(QWeb.render('BscDashboardTemplate', {'bsc': res}))
            })
        },
        });
    core.action_registry.add('bsc_dashboard', BscDashboard);

    return BscDashboard;
});