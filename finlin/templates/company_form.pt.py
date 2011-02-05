registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _attrs_175021484 = _loads('(dp1\n.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_175021868 = _loads('(dp1\n.')
    _attrs_175020332 = _loads('(dp1\n.')
    _attrs_175019084 = _loads('(dp1\nVaction\np2\nV${save_url}\np3\nsVmethod\np4\nVpost\np5\ns.')
    _attrs_175043084 = _loads('(dp1\nVclass\np2\nVfield\np3\ns.')
    _attrs_175018828 = _loads('(dp1\n.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_175042860 = _loads('(dp1\nVclass\np2\nVlabel\np3\ns.')
    _attrs_175018572 = _loads('(dp1\n.')
    _attrs_175020556 = _loads('(dp1\nVclass\np2\nVfield\np3\ns.')
    _attrs_175021228 = _loads('(dp1\nVclass\np2\nVlabel\np3\ns.')
    _attrs_175019692 = _loads('(dp1\n.')
    _attrs_175020012 = _loads('(dp1\nVclass\np2\nVlabel\np3\ns.')
    _attrs_175019372 = _loads('(dp1\n.')
    _attrs_175021932 = _loads('(dp1\nVname\np2\nVanalysis\np3\ns.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_175020748 = _loads('(dp1\n.')
    _attrs_175021676 = _loads('(dp1\nVclass\np2\nVfield\np3\ns.')
    _attrs_175020812 = _loads('(dp1\nVtype\np2\nVtext\np3\nsVname\np4\nVtitle\np5\ns.')
    _attrs_175043340 = _loads('(dp1\nVname\np2\nVsubmit\np3\nsVtype\np4\nVsubmit\np5\nsVvalue\np6\nVSave\np7\ns.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u'_init_stream()'
        (_out, _write, ) = _init_stream()
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        u'main'
        _metal = econtext['main']
        def _callback_body(econtext, _repeat, _out=_out, _write=_write, _domain=_domain, **_ignored):
            if _repeat:
                repeat.update(_repeat)
            attrs = _attrs_175018572
            _write(u'<div>\n    ')
            attrs = _attrs_175018828
            _write(u'<h1>Add a Company</h1>\n    ')
            attrs = _attrs_175019084
            "join(value('save_url'),)"
            _write(u'<form')
            _tmp1 = econtext['save_url']
            if (_tmp1 is _default):
                _tmp1 = u'${save_url}'
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
                _write(((' action="' + _tmp1) + '"'))
            _write(u' method="post">\n\n    ')
            attrs = _attrs_175019372
            _write(u'<table>\n        ')
            attrs = _attrs_175019692
            _write(u'<tr>\n          ')
            attrs = _attrs_175020012
            _write(u'<td class="label">')
            attrs = _attrs_175020332
            _write(u'<label>Name:</label></td>\n          ')
            attrs = _attrs_175020556
            _write(u'<td class="field">')
            attrs = _attrs_175020812
            _write(u'<input name="title" type="text" /></td>\n        </tr>\n        ')
            attrs = _attrs_175020748
            _write(u'<tr>\n          ')
            attrs = _attrs_175021228
            _write(u'<td class="label">')
            attrs = _attrs_175021484
            _write(u'<label>Analysis:</label></td>\n          ')
            attrs = _attrs_175021676
            _write(u'<td class="field">')
            attrs = _attrs_175021932
            _write(u'<textarea name="analysis"></textarea></td>\n        </tr>\n        ')
            attrs = _attrs_175021868
            _write(u'<tr>\n          ')
            attrs = _attrs_175042860
            _write(u'<td class="label"></td>\n          ')
            attrs = _attrs_175043084
            _write(u'<td class="field">')
            attrs = _attrs_175043340
            _write(u'<input type="submit" name="submit" value="Save" /></td>\n        </tr>\n    </table>\n\n    </form>\n  </div>\n')
        u"{'body': _callback_body}"
        _tmp = {'body': _callback_body, }
        u'main'
        _metal.render(_tmp, _out=_out, _write=_write, _domain=_domain, econtext=econtext)
        return _out.getvalue()
    return render

__filename__ = '/home/bobby/py_virtual/Finlin/finlin/templates/company_form.pt'
registry[(None, True, '1488bdb950901f8f258549439ef6661a49aae984')] = bind()
