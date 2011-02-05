registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _attrs_172644556 = _loads('(dp1\nVid\np2\nVdoc\np3\ns.')
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_172644588 = _loads('(dp1\nVxml:lang\np2\nVen\np3\nsVxmlns\np4\nVhttp://www.w3.org/1999/xhtml\np5\ns.')
    _attrs_172643884 = _loads('(dp1\n.')
    _attrs_172085548 = _loads('(dp1\nVid\np2\nVft\np3\ns.')
    _attrs_172716716 = _loads('(dp1\n.')
    _attrs_172645772 = _loads("(dp1\nVmedia\np2\nVscreen\np3\nsVcharset\np4\nVutf-8\np5\nsVhref\np6\nV${request.static_url('finlin:static/reset-fonts-grids.css')}\np7\nsVrel\np8\nVstylesheet\np9\nsVtype\np10\nVtext/css\np11\ns.")
    _attrs_172645932 = _loads("(dp1\nVmedia\np2\nVscreen\np3\nsVcharset\np4\nVutf-8\np5\nsVhref\np6\nV${request.static_url('finlin:static/main.css')}\np7\nsVrel\np8\nVstylesheet\np9\nsVtype\np10\nVtext/css\np11\ns.")
    _attrs_172191020 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_172646220 = _loads('(dp1\nVcontent\np2\nVtext/html;charset=UTF-8\np3\nsVhttp-equiv\np4\nVContent-Type\np5\ns.')
    _attrs_172646316 = _loads("(dp1\nVhref\np2\nV${request.static_url('finlin:static/favicon.ico')}\np3\nsVrel\np4\nVshortcut icon\np5\ns.")
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_172645836 = _loads('(dp1\n.')
    _attrs_172644428 = _loads('(dp1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_172189612 = _loads('(dp1\nVhref\np2\nV/\ns.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u"%(scope)s['%(out)s'], %(scope)s['%(write)s']"
        (_out, _write, ) = (econtext['_out'], econtext['_write'], )
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        _write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
        attrs = _attrs_172644588
        _write(u'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n')
        attrs = _attrs_172643884
        _write(u'<head>\n  ')
        attrs = _attrs_172645836
        _write(u'<title>Finlin</title>\n  ')
        attrs = _attrs_172646220
        _write(u'<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n  ')
        attrs = _attrs_172646316
        'join(value("request.static_url(\'finlin:static/favicon.ico\')"),)'
        _write(u'<link rel="shortcut icon"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('finlin:static/favicon.ico')
        if (_tmp1 is _default):
            _tmp1 = u"${request.static_url('finlin:static/favicon.ico')}"
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u' />\n  ')
        attrs = _attrs_172645772
        'join(value("request.static_url(\'finlin:static/reset-fonts-grids.css\')"),)'
        _write(u'<link rel="stylesheet"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('finlin:static/reset-fonts-grids.css')
        if (_tmp1 is _default):
            _tmp1 = u"${request.static_url('finlin:static/reset-fonts-grids.css')}"
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u' type="text/css" media="screen" charset="utf-8" />\n\n  ')
        attrs = _attrs_172645932
        'join(value("request.static_url(\'finlin:static/main.css\')"),)'
        _write(u'<link rel="stylesheet"')
        _tmp1 = _lookup_attr(econtext['request'], 'static_url')('finlin:static/main.css')
        if (_tmp1 is _default):
            _tmp1 = u"${request.static_url('finlin:static/main.css')}"
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = str(_tmp1)
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' href="' + _tmp1) + '"'))
        _write(u' type="text/css" media="screen" charset="utf-8" />\n</head>\n\n')
        attrs = _attrs_172644428
        _write(u'<body>\n  ')
        attrs = _attrs_172644556
        u"%(slots)s.get(u'body')"
        _write(u'<div id="doc">\n    ')
        _tmp = _slots.get(u'body')
        u'%(tmp)s is not None'
        _tmp1 = (_tmp is not None)
        if _tmp1:
            pass
            u'isinstance(%(tmp)s, basestring)'
            _tmp2 = isinstance(_tmp, basestring)
            if not _tmp2:
                pass
                econtext.update(dict(rcontext=rcontext, _domain=_domain))
                _tmp(econtext, repeat)
            else:
                pass
                u'%(tmp)s'
                _tmp2 = _tmp
                _tmp = _tmp2
                if (_tmp.__class__ not in (str, unicode, int, float, )):
                    try:
                        _tmp = _tmp.__html__
                    except:
                        _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                    else:
                        _tmp = _tmp()
                        _write(_tmp)
                        _tmp = None
                if (_tmp is not None):
                    if not isinstance(_tmp, unicode):
                        _tmp = str(_tmp)
                    _write(_tmp)
        else:
            pass
            attrs = _attrs_172716716
            _write(u'<p>\n      This is the body.\n    </p>')
        _write(u'\n\n    ')
        attrs = _attrs_172085548
        _write(u'<div id="ft">\n      ')
        attrs = _attrs_172191020
        _write(u'<p>\n        &copy; Finlin 2011\n        ')
        attrs = _attrs_172189612
        _write(u'<a href="/">[Home]</a> |\n      </p>        \n    </div>\n  </div>\n</body>\n</html>')
        return
    return render

__filename__ = '/home/bobby/py_virtual/Finlin/finlin/templates/master.pt'
registry[('', False, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
