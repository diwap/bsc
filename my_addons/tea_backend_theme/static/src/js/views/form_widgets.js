odoo.define('tea_backend_theme.form_widgets', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var form_widgets = require('web.form_widgets');

    var QWeb = core.qweb;

    form_widgets.FieldStatus.include({
        template: undefined,
        className: "o_statusbar_status",
        render_value: function() {
            var self = this;
            var $content = $(QWeb.render("FieldStatus.content." + ((config.device.size_class <= config.device.SIZES.XS)? 'mobile' : 'desktop'), {
                'widget': this,
                'value_folded': _.find(this.selection.folded, function (i) {
                    return i[0] === self.get('value');
                }),
            }));
            this.$el.empty().append($content.get().reverse());
        },
        bind_stage_click: function () {
            this.$el.on('click','button[data-id]',this.on_click_stage);
        },
    });

    var FieldPhone = form_widgets.FieldEmail.extend({
        prefix: 'tel',
        init: function() {
            this._super.apply(this, arguments);
            this.clickable = config.device.size_class <= config.device.SIZES.XS;
        },
        render_value: function() {
            this._super();
            if(this.clickable) {
                var text = this.$el.text();
                this.$el.html(text.substr(0, text.length/2) + "&shy;" + text.substr(text.length/2)); // To prevent Skype app to find the phone number
            }
        }
    });

    core.form_widget_registry
        .add('phone', FieldPhone)
        .add('upgrade_boolean', form_widgets.FieldBoolean) // community compatibility
        .add('upgrade_radio', form_widgets.FieldRadio); // community compatibility

});


odoo.define('tea_backend_theme.form_upgrade_widgets', function (require) {
"use strict";

var core = require('web.core');
var Dialog = require('web.Dialog');
var form_widgets = require('web.form_widgets');
var framework = require('web.framework');
var Model = require('web.DataModel');

var _t = core._t;
var QWeb = core.qweb;

/**
 *  This widget is intended to be used in config settings.
 *  When checked, an upgrade popup is showed to the user.
 */
var AbstractFieldUpgrade = {
    events: {
        'click input': 'on_click_input',
    },

    start: function() {
        this._super.apply(this, arguments);
        this.get_enterprise_label().after($("<span>", {
            text: "Enterprise",
            'class': "label label-primary oe_inline"
        }));
    },

    open_dialog: function() {
        var message = $(QWeb.render('EnterpriseUpgrade'));

        var buttons = [
            {
                text: _t("Upgrade now"),
                classes: 'btn-primary',
                close: true,
                click: this.confirm_upgrade,
            },
            {
                text: _t("Cancel"),
                close: true,
            },
        ];

        return new Dialog(this, {
            size: 'medium',
            buttons: buttons,
            $content: $('<div>', {
                html: message,
            }),
            title: _t("Odoo Enterprise"),
        }).open();
    },

    confirm_upgrade: function() {
        new Model("res.users").call("search_count", [[["share", "=", false]]]).then(function(data) {
            framework.redirect("https://www.odoo.com/odoo-enterprise/upgrade?num_users=" + data);
        });
    },

    get_enterprise_label: function() {},
    on_click_input: function() {},
};

var UpgradeBoolean = form_widgets.FieldBoolean.extend(AbstractFieldUpgrade, {
    template: "FieldUpgradeBoolean",

    get_enterprise_label: function() {
        return this.$label;
    },

    on_click_input: function() {
        if(this.$checkbox.prop("checked")) {
            this.open_dialog().on('closed', this, function() {
                this.$checkbox.prop("checked", false);
            });
        }
    },
});

var UpgradeRadio = form_widgets.FieldRadio.extend(AbstractFieldUpgrade, {
    get_enterprise_label: function() {
        // override the margin:0px
        this.$('label').addClass('mr4');
        return this.$('label').last();
    },
    on_click_input: function(event) {
        if($(event.target).val() === "1") {
            this.open_dialog().on('closed', this, function() {
                this.$('input').first().prop("checked", true);
            });
        }
    },
});

core.form_widget_registry
    .add('upgrade_boolean', UpgradeBoolean)
    .add('upgrade_radio', UpgradeRadio);

});