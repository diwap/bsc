odoo.define('tea_backend_theme.ViewManager', function (require) {
    "use strict";

    var config = require('web.config');
    var ViewManager = require('web.ViewManager');

    ViewManager.include({
        /**
         * Special case for mobile mode: if there is one, use a mobile-friendly view as default view
         *
         * @returns {Object} the default view
         */
        get_default_view: function () {
            var default_view = this._super.apply(this, arguments);
            if (config.device.size_class <= config.device.SIZES.XS && !default_view.mobile_friendly) {
                default_view = (_.find(this.views, function (v) { return v.mobile_friendly; })) || default_view;
            }
            return default_view;
        },
    });

});
