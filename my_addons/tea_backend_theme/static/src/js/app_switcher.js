odoo.define('tea_backend_theme.AppSwitcher', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var Widget = require('web.Widget');

    var QWeb = core.qweb;
    var NBR_ICONS = 6;

    function visit(tree, callback, path) {
        path = path || [];
        callback(tree, path);
        _.each(tree.children, function(node) {
            visit(node, callback, path.concat(tree));
        });
    }

    function is_mobile() {
        return config.device.size_class <= config.device.SIZES.XS;
    }

    var AppSwitcher = Widget.extend({
        template: 'AppSwitcher',
        events: {
            'input input.o_menu_search_input': function(e) {
                if(!e.target.value) {
                    this.state = this.get_initial_state();
                    this.state.is_searching = true;
                }
                this.update({search: e.target.value, focus: 0});
            },
            'click .o_menuitem': 'on_menuitem_click',
        },
        init: function (parent, menu_data) {
            this._super.apply(this, arguments);
            this.menu_data = this.process_menu_data(menu_data);
            this.state = this.get_initial_state();
        },
        start: function () {
            this.$input = this.$('input');
            this.$menu_search = this.$('.o_menu_search');
            this.$main_content = this.$('.o_application_switcher_scrollable');
            return this._super.apply(this, arguments);
        },
        get_initial_state: function () {
            return {
                apps: _.where(this.menu_data, {is_app: true}),
                menu_items: [],
                focus: null,  // index of focused element
                is_searching: is_mobile(),
            };
        },
        process_menu_data: function(menu_data) {
            var result = [];
            visit(menu_data, function (menu_item, parents) {
                if (!menu_item.id || !menu_item.action) {
                    return;
                }
                var item = {
                    label: _.pluck(parents.slice(1), 'name').concat(menu_item.name).join(' / '),
                    id: menu_item.id,
                    xmlid: menu_item.xmlid,
                    action: menu_item.action ? menu_item.action.split(',')[1] : '',
                    is_app: !menu_item.parent_id,
                    web_icon: menu_item.web_icon,
                };
                if (!menu_item.parent_id) {
                    if (menu_item.web_icon_data) {
                        item.web_icon_data = 'data:image/png;base64,' + menu_item.web_icon_data;
                    } else if (item.web_icon) {
                        var icon_data = item.web_icon.split(',');
                        var $icon = $('<div>')
                            .addClass('o_app_icon')
                            .css('background-color', icon_data[2])
                            .append(
                                $('<i>')
                                    .addClass(icon_data[0])
                                    .css('color', icon_data[1])
                            );
                        item.web_icon = $icon[0].outerHTML;
                    } else {
                        item.web_icon_data = '/tea_backend_theme/static/src/img/default_icon_app.png';
                    }
                } else {
                    item.menu_id = parents[1].id;
                }
                result.push(item);
            });
            return result;
        },
        on_attach_callback: function () {
            core.bus.on("keydown", this, this.on_keydown);
            this.state = this.get_initial_state();
            this.$input.val('');
            this.render();
        },
        on_detach_callback: function () {
            core.bus.off("keydown", this, this.on_keydown);
        },
        get_app_index: function () {
            return this.state.focus < this.state.apps.length ? this.state.focus : null;
        },
        get_menu_index: function () {
            var state = this.state;
            return state.focus >= state.apps.length ? state.focus - state.apps.length : null;
        },
        on_keydown: function(event) {
            var is_editable = event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA" || event.target.isContentEditable;
            if (is_editable && event.target !== this.$input[0]) {
                return;
            }
            var state = this.state;
            var elem_focused = state.focus !== null;
            var app_focused = elem_focused && state.focus < state.apps.length;
            var delta = app_focused ? NBR_ICONS : 1;
            var $input = this.$input;
            switch (event.which) {
                case $.ui.keyCode.DOWN:
                    this.update({focus: elem_focused ? delta : 0});
                    event.preventDefault();
                    break;
                case $.ui.keyCode.RIGHT:
                    if ($input.is(':focus') && $input[0].selectionEnd < $input.val().length) {
                        return;
                    }
                    this.update({focus: elem_focused ? 1 : 0});
                    event.preventDefault();
                    break;
                case $.ui.keyCode.TAB:
                    event.preventDefault();
                    var f = elem_focused ? (event.shiftKey ? -1 : 1) : 0;
                    this.update({focus: f});
                    break;
                case $.ui.keyCode.UP:
                    this.update({focus: elem_focused ? -delta : 0});
                    event.preventDefault();
                    break;
                case $.ui.keyCode.LEFT:
                    if ($input.is(':focus') && $input[0].selectionStart > 0) {
                        return;
                    }
                    this.update({focus: elem_focused ? -1 : 0});
                    event.preventDefault();
                    break;
                case $.ui.keyCode.ENTER:
                    if (elem_focused) {
                        var menus = app_focused ? state.apps : state.menu_items;
                        var index = app_focused ? state.focus : state.focus - state.apps.length;
                        this.open_menu(menus[index]);
                    }
                    event.preventDefault();
                    return;
                case $.ui.keyCode.PAGE_DOWN:
                case $.ui.keyCode.PAGE_UP:
                    break;
                default:
                    if (!this.$input.is(':focus')) {
                        this.$input.focus();
                    }
            }
        },
        on_menuitem_click: function (e) {
            e.preventDefault();
            var menu_id = $(e.currentTarget).data('menu');
            this.open_menu(_.findWhere(this.menu_data, {id: menu_id}));
        },
        update: function(data) {
            var self = this;
            if (data.search) {
                var options = {extract: function(el) { return el.label; }};
                var search_results = fuzzy.filter(data.search, this.menu_data, options);
                var results = _.map(search_results, function (result) {
                    return self.menu_data[result.index];
                });
                this.state = _.extend(this.state, {
                    apps: _.where(results, {is_app: true}),
                    menu_items: _.where(results, {is_app: false}),
                    focus: results.length ? 0 : null,
                    is_searching: true,
                });
            }
            if (this.state.focus !== null && 'focus' in data) {
                var state = this.state;
                var app_nbr = state.apps.length;
                var new_index = data.focus + (state.focus || 0);
                if (new_index < 0) {
                    new_index = state.apps.length + state.menu_items.length - 1;
                }
                if (new_index >= state.apps.length + state.menu_items.length) {
                    new_index = 0;
                }
                if (new_index >= app_nbr && state.focus < app_nbr && data.focus > 0) {
                    if (state.focus + data.focus - (state.focus % data.focus) < app_nbr) {
                        new_index = app_nbr - 1;
                    } else {
                        new_index = app_nbr;
                    }
                }
                if (new_index < app_nbr && state.focus >= app_nbr && data.focus < 0) {
                    new_index = app_nbr - (app_nbr % NBR_ICONS);
                    if (new_index === app_nbr) {
                        new_index = app_nbr - NBR_ICONS;
                    }
                }
                state.focus = new_index;
            }
            this.render();
        },
        render: function() {
            this.$menu_search.toggleClass('o_bar_hidden', !this.state.is_searching);
            this.$main_content.html(QWeb.render('AppSwitcher.Content', { widget: this }));
            var $focused = this.$main_content.find('.o_focused');
            if ($focused.length && !is_mobile()) {
                $focused.focus();
                this.$el.scrollTo($focused, {offset: {top:-0.5*this.$el.height()}});
            }

            var offset = window.innerWidth - (this.$main_content.offset().left * 2 + this.$main_content.outerWidth());
            if (offset) {
                this.$el.css('padding-left', "+=" + offset);
            }
        },
        open_menu: function(menu) {
            this.trigger_up(menu.is_app ? 'app_clicked' : 'menu_clicked', {
                menu_id: menu.id,
                action_id: menu.action,
            });
            if (!menu.is_app) {
                core.bus.trigger('change_menu_section', menu.menu_id);
            }
        }
    });

    return AppSwitcher;

});

