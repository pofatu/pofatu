<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%def name="sidebar()">
    <div class="well">
        <h4>Source</h4>
        ${h.link(req, ctx.source, label=ctx.source.name)}.
        ${h.link(req, ctx.source, label=ctx.source.description)}
        <h4>Description</h4>
        <p>${ctx.description}</p>
    </div>
</%def>

<h2>${_('Contribution')} ${ctx.name}</h2>

${util.data()}

<% dt = request.get_datatable('values', h.models.Value, contribution=ctx) %>
% if dt:
<div>
    ${dt.render()}
</div>
% endif
