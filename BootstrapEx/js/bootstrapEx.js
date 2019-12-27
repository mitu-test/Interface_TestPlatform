var bootstrapEx = {};
bootstrapEx.language = {
    Modal: {
        title: function () { return "窗口标题"; },
        closebtn: function () { return "关闭"; }
    }
};
(function ($) {
    doCallback = function (fn, args) {
        return fn.apply(this, args);
    }

    //modal弹出层
    Modal = function () {
        var _Modal = {
            renderto: "",//绘制ID
            header: null,//头元素
            body: null,//body元素
            footer: null,//footer元素
            btns: [],//按钮组
            title: bootstrapEx.language.Modal.title(),//title
            showclosebtn: true,//显示关闭按钮
            InitMax: true,//是否最大化
            firstInit: false,
            setHeigth: function (h) {
                var t = this;
                $(t.renderto).find('.modal-body').css('min-height', h);// - 110 * 2
                $(window).resize(function () {
                    $(t.renderto).find('.modal-body').css('min-height', h);// - 110 * 2
                });
            },//设置高度
            setWidth: function (w) {
                var t = this;
                $(t.renderto).find('.modal-dialog').css('width', w);// - 200 * 2
                $(window).resize(function () {
                    $(t.renderto).find('.modal-dialog').css('width', w);// - 200 * 2
                });
            },//设置宽度
            modal: { show: true, backdrop: 'static' },
            Init: function (isshow) {
                var t = this;
                $(t.renderto).html('');
                var body = t.body;
                t.header = null;
                t.body = null;
                t.footer = null;
                if (!$(t.renderto).hasClass('modal')) {
                    $(t.renderto).addClass('modal');
                }
                if (!$(t.renderto).hasClass('fade')) {
                    $(t.renderto).addClass('fade');
                }
                $(t.renderto).append('<div class="modal-dialog"><div class="modal-content"></div></div>');
                t.header = $('<div class="modal-header"></div>');
                if (t.showclosebtn) {
                    $(t.header).append('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>');
                }
                $(t.header).append('<div class="modal-title">' + t.title + '</div>');
                $(t.renderto).find(".modal-content").append(t.header);
                t.body = $('<div class="modal-body"></div>');
                $(t.renderto).find(".modal-content").append(t.body);
                t.body.append(body);
                t.footer = $('<div class="modal-footer"></div>');
                $(t.renderto).find(".modal-content").append(t.footer);
                t.btns.forEach(function (btn) {
                    var btnclass = btn.class || "btn-primary";
                    var _b = "";
                    if (btn.id != "closebtn") {
                        _b = $('<button class="btn" type="button"  id="' + btn.id + '">' + btn.text + '</button>');
                        $(_b).addClass(btnclass);
                    } else {
                        _b = $('<button class="btn btn-default" type="button" data-dismiss="modal" aria-hidden="true" id="' + btn.id + '">' + bootstrapEx.language.Modal.closebtn() + '</button>');
                    }
                    $(t.footer).append(_b);
                }, this);
                if (t.InitMax) {
                    $(t.renderto).find('.modal-dialog').css('width', $(window).width() - 150 * 2);// - 200 * 2
                    $(t.renderto).find('.modal-body').css('min-height', $(window).height() - 110 * 2);// - 150 * 2
                }
                if (isshow) {
                    var moopt = { show: true, backdrop: 'static' };//keyboard
                    moopt = $.extend(moopt, t.modal);
                    $(t.renderto).modal(moopt);
                }
                $(t.renderto).on('shown.bs.modal', function () {
                    try {
                        eval(t.renderto.replace("#", "").replace(".", "") + "_Show();");
                    } catch (ex) { }
                })

                $(t.renderto).on('hide.bs.modal', function () {
                    try {
                        eval(t.renderto.replace("#", "").replace(".", "") + "_Hide();");
                    } catch (ex) { }
                })
                $(t.renderto).on('hidden.bs.modal', function () {
                    try {
                        eval(t.renderto.replace("#", "").replace(".", "") + "_Hideend();");
                    } catch (ex) { }
                })
                t.firstInit = true;
                doCallback(t.OnfirstInited, [t]);
            },
            setTitle: function (title) {//设置标题
                var t = this;
                t.title = title;
                $(t.header).find('.modal-title').html(t.title);
            },
            toggle: function () {//设置是否显示
                var t = this;
                $(t.renderto).modal('toggle');
            },
            show: function () {//显示
                var t = this;
                if (!t.firstInit) {
                    t.Init();
                }
                var moopt = { show: true, backdrop: 'static' };//keyboard
                moopt = $.extend(moopt, t.modal);
                $(t.renderto).modal(moopt);
            },
            hide: function () {//关闭
                var t = this;
                $(t.renderto).modal('hide');
            },
            OnfirstInited: function () {

            }


        }
        return _Modal;
    }
    //页签tab
    Tab = function () {
        var tabdefault = function () {
            var _tab = {
                id: "",//id
                title: "",//标题
                url: "",//地址
                isiframe: false,//是否生成ifram
                active: false,//是否激活
                iframe: null,//ifram
                iframefn: null,//返回ifram 的中的contentWindow对象 执行function 返回
                tabel: null,//页签元素
                bodyel: null,//body元素
                load: null,//load 事件触发
                showclosebtn: false
            }; return _tab;
        }
        var _tabs = {
            renderto: "",//绘制ID
            navtabs: null,
            tabcontent: null,
            tabs: [],
            fade: true,//是否显示过度效果
            firstInit: false,
            show: function (tab) {
                var tabindex;
                var t = this;
                if (!t.firstInit) {
                    t.init();
                }
                if (typeof tab == "number") {
                    tabindex = parseInt(tab);
                }
                else if (typeof tab == "object") {
                    tabindex = t.tabs.indexOf(tab);
                }
                $(t.renderto).find('li').removeClass('active');
                $(t.renderto).find('div.tab-pane').removeClass('active');
                if ($(t.renderto).find('li').eq(tabindex).css("display") == 'none') {
                    $(t.renderto).find('li').eq(tabindex).css("display", "inline");
                }
                $(t.renderto).find('li').eq(tabindex).addClass('active');
                $(t.renderto).find('div.tab-pane').eq(tabindex).addClass('active');
                if ($(t.renderto).find('div.tab-pane').eq(tabindex).hasClass('fade') && !$(t.renderto).find('div.tab-pane').eq(tabindex).hasClass('in')) {
                    $(t.renderto).find('div.tab-pane').eq(tabindex).addClass('in');
                }
                if (t.tabs && t.tabs[tabindex] && t.tabs[tabindex].id) {
                    eval("var fun;try{fun=" + t.tabs[tabindex].id + "_onactive;}catch(ex){}");
                    if (fun) {
                        fun(t);
                    }
                }
            },
            hide: function (tab) {
                var tabindex;
                var t = this;
                if (typeof tab == "number") {
                    tabindex = parseInt(tab);
                }
                else if (typeof tab == "object") {
                    tabindex = t.tabs.indexOf(tab);
                }
                if (t.tabs.length == 1 && tabindex == 0) { return };
                $(t.renderto).find('li').eq(tabindex).css("display", "none");
                //隐藏后显示后一个，如果后一个本来就隐藏就显示再后一个
                for (var k = tabindex - 1; k >= 0 && k <= t.tabs.length - tabindex; k--) {
                    if ($(t.renderto).find('li').eq(k).css("display") != 'none') {
                        t.show(k);
                        break;
                    }
                }
                if (t.tabs && t.tabs[tabindex] && t.tabs[tabindex].id) {
                    eval("var fun;try{fun=" + t.tabs[tabindex].id + "_onhide;}catch(ex){}");
                    if (fun) {
                        fun(t);
                    }
                }
            },
            Init: function () {//绘制方法
                var t = this;
                t.navtabs = $('<ul class="nav nav-tabs"></ul>');
                t.tabcontent = $('<div class="tab-content"></div>');
                $(t.renderto).append(t.navtabs);
                $(t.renderto).append(t.tabcontent);
                var is_active = false;
                $.each(t.tabs, function (i, _tab) {
                    tab = $.extend(tabdefault(), _tab);
                    tab.tabel = $('<li> <a data-toggle="tab" href="#' + tab.id + '" >' + tab.title + '</a></li>');
                    if (tab.showclosebtn) {
                        tab.tabel = $('<li> <a data-toggle="tab" style="padding-right:25px;" href="#' + tab.id + '" >' + tab.title
                            + '&nbsp;<i class="glyphicon glyphicon-remove small" tabsindex="' + i + '" id="tabclose_' + i + '" style="position: absolute;top: 14px;cursor: pointer; opacity: 0.3;" ></i></a></li>');
                    }
                    var bodyel = tab.bodyel;
                    tab.bodyel = $('<div class="tab-pane" id="' + tab.id + '"></div>');
                    if (tab.isiframe) {
                        tab.iframe = $('<iframe id="' + tab.id + '_iframe" width="100%" height="100%" src="' + tab.url + '" frameborder="0"></iframe>');
                        $(tab.bodyel).append(tab.iframe);
                    }
                    if (t.fade) {
                        $(tab.bodyel).addClass("fade");
                        $(tab.bodyel).addClass("in");
                    }
                    if (!is_active && tab.active) {
                        is_active = true;
                        $(tab.tabel).addClass("active");
                        $(tab.bodyel).addClass("active");
                    }
                    $(t.navtabs).append(tab.tabel);
                    $(t.tabcontent).append(tab.bodyel);
                    tab.bodyel.append(bodyel);
                    t.tabs[i] = tab;
                    if (document.getElementById(tab.id + '_iframe') && document.getElementById(tab.id + '_iframe').contentWindow) {
                        tab.iframefn = document.getElementById(tab.id + '_iframe').contentWindow;
                    }
                    tab.iframe = $('#' + tab.id + '_iframe');
                    var load;
                    if (tab.load) {
                        load = tab.load;
                        $('#' + tab.id + '_iframe').load(function () {
                            load(this);
                        });
                    }
                })
                //$(t.renderto).find('.tab-pane').css('min-height', $(t.renderto).height());
                setTimeout(function () {
                    $(t.renderto).find('.tab-pane').find('iframe').css('min-height', $(window).height() - 140 * 2);
                }, 200);
                $(t.navtabs).find('[tabsindex]').on('click', function () {
                    t.hide(parseInt($(this).attr('tabsindex')));
                    return false;
                })
                t.firstInit = true;
                doCallback(t.OnfirstInited, [t]);
            },
            isactive: function (tab) {
                var tabindex;
                var t = this;
                if (typeof tab == "number") {
                    tabindex = parseInt(tab);
                }
                else if (typeof tab == "object") {
                    tabindex = t.tabs.indexOf(tab);
                }
                if (tabindex == 0) { return };
                return $(t.renderto).find('li').eq(tabindex).css("display") != 'none';
            },
            OnfirstInited: function () {
            }
        };
        return _tabs;
    }
    getNowDateInt = function () {
        var date = new Date();
        var seperator1 = "-";
        var seperator2 = ":";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        if (month >= 1 && month <= 9) {
            month = "0" + month;
        }
        if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
        }
        var currentdate = date.getFullYear() + month + strDate
            + date.getHours() + date.getMinutes()
            + date.getSeconds();
        return currentdate;
    }

})(jQuery);
