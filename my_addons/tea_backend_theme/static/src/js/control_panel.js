odoo.define('tea_backend_theme.ControlPanel', function (require) {
    "use strict";

    var config = require('web.config');
    var ControlPanel = require('web.ControlPanel');

    ControlPanel.include({
        _render_breadcrumbs_li: function (bc, index, length) {
            var $bc = this._super.apply(this, arguments);

            var is_last = (index === length-1);
            var is_before_last = (index === length-2);

            $bc.toggleClass('hidden-xs', !is_last && !is_before_last)
                .toggleClass('o_back_button', is_before_last);

            return $bc;
        },
        _update_search_view: function(searchview, is_hidden) {
            this._super.apply(this, arguments);

            if (config.device.size_class <= config.device.SIZES.XS) {
                this.$el.addClass('o_breadcrumb_full');
            }

            if(this.$enable_searchview === undefined) {
                var self = this;
                this.$enable_searchview = $('<button/>', {type: 'button'})
                    .addClass('o_enable_searchview btn btn-sm btn-default fa fa-search')
                    .on('click', function() {
                        self.searchview_displayed = !self.searchview_displayed;
                        self.$el.toggleClass('o_breadcrumb_full', !self.searchview_displayed);
                        self.nodes.$searchview_buttons.toggle(self.searchview_displayed);
                    });
            }
            if(!is_hidden && config.device.size_class <= config.device.SIZES.XS) {
                this.$enable_searchview.insertAfter(this.nodes.$searchview);
                this.searchview_displayed = false;
                this.nodes.$searchview_buttons.hide();
            } else {
                this.$enable_searchview.detach();
            }
        },
    });

    return ControlPanel;

});
