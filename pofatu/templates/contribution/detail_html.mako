<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%def name="sidebar()">
    <div class="well">
        <h4>Sources</h4>
        <ul>
            % for ref in ctx.references:
                <li>
                    ${h.link(req, ref.source, label=ref.source.name)}.
                    ${h.link(req, ref.source, label=ref.source.description)}
                </li>
            % endfor
        </ul>
    </div>
</%def>

<h2>${ctx.name}</h2>
<p>${ctx.description}</p>


${util.data()}

<% dt = request.get_datatable('values', h.models.Value, contribution=ctx) %>
% if dt:
<div>
    ${dt.render()}
</div>
% endif
