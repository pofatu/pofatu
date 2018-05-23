<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "rocksources" %>
<%block name="title">${ctx.type} ${ctx.name}</%block>

<h2>${title()}</h2>
