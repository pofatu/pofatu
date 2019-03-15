<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<%def name="sidebar()">
    <div class="well">
        <dl>
            <dt>Location:</dt>
            <dd>${h.link(request, ctx.valueset.language)}</dd>
            <dt>Sample type:</dt>
            <dd>${h.link(request, ctx.valueset.parameter)}</dd>
        </dl>
    </div>
    <div class="well">
        <h4>Sources</h4>
        <dl>
        % for type_, sources in ctx.iter_grouped_sources():
            <dt>${type_.capitalize()}</dt>
            <dd>
                <ul class="unstyled">
                    % for source in sources:
                        <li>${h.link(request, source)}</li>
                    % endfor
                </ul>
            </dd>
        % endfor
        </dl>
    </div>
</%def>


<h2>${_('Value')} ${ctx.name}</h2>

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'measurements'); dt = dt(request, u.Measurement, sample=ctx) %>
    ${dt.render()}
</div>
