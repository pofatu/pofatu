<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "rocksources" %>
<%block name="title">Sources</%block>

<h2>Sources</h2>

${req.get_map().render()}

${ctx.render()}
