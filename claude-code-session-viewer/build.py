#!/usr/bin/env python3
"""CCViewer 多语言静态页构建：src/template.html + src/i18n/*.json -> 10 个语言页。
用法: python3 build.py
输出: index.html (en, 默认) + <lang>/index.html ×9
"""
import json, html, re, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ['en','zh','ja','ko','es','fr','de','pt','ru','hi']
OG_LOCALE = {'en':'en_US','zh':'zh_CN','ja':'ja_JP','ko':'ko_KR','es':'es_ES',
             'fr':'fr_FR','de':'de_DE','pt':'pt_BR','ru':'ru_RU','hi':'hi_IN'}
SITE = 'https://ccviewer.top/claude-code-session-viewer'

REDIRECT_JS = ("<script>(function(){try{var LS=['zh','ja','ko','es','fr','de','pt','ru','hi'];"
 "var p=null;try{p=localStorage.getItem('ccviewer_pref');}catch(e){}"
 "if(p){if(p!=='en'&&LS.indexOf(p)>=0)location.replace('/claude-code-session-viewer/'+p+'/');return;}"
 "var nl=navigator.languages||(navigator.language?[navigator.language]:[]);"
 "for(var i=0;i<nl.length;i++){var l=String(nl[i]).toLowerCase().split('-')[0];"
 "if(l==='en')return;"
 "if(LS.indexOf(l)>=0){try{localStorage.setItem('ccviewer_pref',l);}catch(e){}"
 "location.replace('/claude-code-session-viewer/'+l+'/');return;}}}catch(e){}})();</script>")

def url_for(lang):
    return SITE + '/' if lang == 'en' else f'{SITE}/{lang}/'

def strip_tags(s):
    return H.unescape(re.sub(r'<[^>]+>', '', s))

def bake(html_str, ui):
    """把 locale 文案烘进静态 HTML（保留 data-i18n 属性，运行时 applyLang 会填同样内容）"""
    def rep(m):
        tag, attrs, key, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        val = ui.get(key, inner)
        if 'data-i18n-html' not in attrs:
            val = H.escape(str(val), quote=False)
        return f'<{tag}{attrs}>{val}</{tag}>'
    return re.sub(r'<(?P<tag>[a-zA-Z][a-zA-Z0-9]*)([^>]*data-i18n(?:-html)?="(?P<key>[^"]+)"[^>]*)>([\s\S]*?)</(?P=tag)>', rep, html_str)

def build():
    tpl = open(os.path.join(HERE,'src/template.html'),encoding='utf-8').read()
    # hreflang 全组（10 语言 + x-default）
    hreflang = '\n'.join(
        f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'

    for lang in LANGS:
        loc = json.load(open(os.path.join(HERE,'src/i18n',f'{lang}.json'),encoding='utf-8'))
        ui = loc['ui']
        url = url_for(lang)
        webapp_ld = json.dumps({
            '@context':'https://schema.org','@type':'WebApplication',
            'name':'CCViewer','url':url,'applicationCategory':'DeveloperApplication',
            'operatingSystem':'Any','browserRequirements':'Requires JavaScript',
            'description':loc['app_desc'],'inLanguage':loc['lang_tag'],
            'offers':{'@type':'Offer','price':'0','priceCurrency':'USD'},
        }, ensure_ascii=False)
        faqs=[]
        for i in range(1,6):
            q=strip_tags(ui['q%d'%i]); a=strip_tags(ui['a%d'%i])
            faqs.append({'@type':'Question','name':q,
                         'acceptedAnswer':{'@type':'Answer','text':a}})
        faq_ld = json.dumps({
            '@context':'https://schema.org','@type':'FAQPage','mainEntity':faqs,
        }, ensure_ascii=False)

        page = tpl
        for k,v in {
            '{{lang_tag}}':loc['lang_tag'],'{{title}}':loc['title'],
            '{{description}}':H.escape(loc['description'],quote=True),
            '{{keywords}}':H.escape(loc['keywords'],quote=True),
            '{{url}}':url,'{{hreflang}}':hreflang,
            '{{og_title}}':H.escape(loc['og_title'],quote=True),
            '{{og_desc}}':H.escape(loc['og_desc'],quote=True),
            '{{og_locale}}':OG_LOCALE[lang],
            '{{webapp_ld}}':webapp_ld,'{{faq_ld}}':faq_ld,
            '{{redirect}}':REDIRECT_JS if lang=='en' else '',
            "'{{lang}}':{{ui}}":f"'{lang}':"+json.dumps(ui,ensure_ascii=False),
            "const LANG='{{lang}}'":f"const LANG='{lang}'",
        }.items():
            page = page.replace(k,v)
        page = bake(page, ui)

        out = os.path.join(HERE,'index.html') if lang=='en' else os.path.join(HERE,lang,'index.html')
        os.makedirs(os.path.dirname(out),exist_ok=True)
        open(out,'w',encoding='utf-8').write(page)
        print('built',out)
    print('done.')

if __name__=='__main__':
    build()
