
odoo.define('login', function (require) {
    "use strict";
    var Login = function () {

        var handleLogin = function() {
            //数据库切换
            var currentdb = $("#db_list option:selected").val()
            $("#db_list").unbind('change');
            $(document).ready(function() {
                $("#db_list").change(function() {
                    if(this.value != currentdb)
                        window.location.href= '/web?db='+this.value;
                })
            });

            function format(db) {
                if (!db.id) {
                    return db.text;
                }
                var $db = $(
                    '<span><i class="fa fa-database"></i> ' + db.text + '</span>'
                );
                return $db;
            }

            if (jQuery().select2 && $('#db_list').size() > 0) {
                $("#db_list").select2({
                    placeholder: '<i class="fa fa-database"></i>',
                    templateResult: format,
                    templateSelection: format,
                    width: 'auto',
                    escapeMarkup: function(m) {
                        return m;
                    }
                });
            }


            //登录验证
            $('.login-form').validate({
                errorElement: 'span', //default input error message container
                errorClass: 'help-block', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                rules: {
                    login: {
                        required: true
                    },
                    password: {
                        required: true
                    }
                },

                messages: {
                    login: {
                        required: "Email is required."
                    },
                    password: {
                        required: "Password is required."
                    }
                },

                invalidHandler: function (event, validator) { //display error alert on form submit
                    $('.alert-danger', $('.login-form')).show();
                },

                highlight: function (element) { // hightlight error inputs
                    $(element)
                        .closest('.form-group').addClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    label.closest('.form-group').removeClass('has-error');
                    label.remove();
                },

                errorPlacement: function (error, element) {
                    error.insertAfter(element.closest('.input-icon'));
                },

                submitHandler: function (form) {
                    form.submit();
                }
            });

            $('.login-form input').keypress(function (e) {
                if (e.which == 13) {
                    if ($('.login-form').validate().form()) {
                        $('.login-form').submit();
                    }
                    return false;
                }
            });
        }


        return {
            //main function to initiate the module
            init: function () {
                handleLogin();

                // init background slide images
                $.backstretch([
                        "/tea_backend_theme/static/src/img/bg/1.jpg",
                        "/tea_backend_theme/static/src/img/bg/2.jpg",
                        "/tea_backend_theme/static/src/img/bg/3.jpg",
                        "/tea_backend_theme/static/src/img/bg/4.jpg"
                    ], {
                        fade: 1000,
                        duration: 8000
                    }
                );
            }
        };
    }();

    jQuery(document).ready(function() {
        Login.init();
    });

});