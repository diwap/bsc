odoo.define('tea_backend_theme.DebugManager', function (require) {
    "use strict";

    var core = require('web.core');
    var WebClient = require('web.WebClient');

    if (core.debug) {
        WebClient.include({
            start: function() {
                var self = this;
                return this._super.apply(this, arguments).then(function () {
                    // Override toggle_app_switcher to trigger an event to update the debug manager's state
                    var toggle_app_switcher = self.toggle_app_switcher;
                    self.toggle_app_switcher = function(display) {
                        var action;
                        if (!display) {
                            action = self.action_manager.get_inner_action();
                        }
                        self.current_action_updated(action);
                        toggle_app_switcher.apply(self, arguments);
                    };
                });
            },
            instanciate_menu_widgets: function() {
                var self = this;
                return this._super.apply(this, arguments).then(function() {
                    // Compatibility with community debug manager
                    self.systray_menu = self.menu.systray_menu;
                });
            },
        });
    }

});
