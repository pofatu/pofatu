<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<%def name="sidebar()">
    <%util:well title="Location">
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
        <dl>
            % if ctx.elevation:
                <dt>Elevation</dt>
                <dd>${ctx.elevation}</dd>
            % endif
            % if ctx.location_comment:
                <dt>Comment</dt>
                <dd>${ctx.location_comment}</dd>
            % endif
            <dd>${h.link(request, ctx.valueset.language)}</dd>
        </dl>
    </%util:well>
    <%util:well title="Site">
        <dl>
            % if ctx.site:
                <dt>Name</dt>
                <dd>${ctx.site.name}</dd>
            % endif
            % if ctx.site_context:
                <dt>Context</dt>
                <dd>${ctx.site_context}</dd>
            % endif
            % if ctx.site_comment:
                <dt>Comment</dt>
                <dd>${ctx.site_comment}</dd>
            % endif
            % if ctx.site_stratigraphic_position:
                <dt>Stratigraphic position</dt>
                <dd>${ctx.site_stratigraphic_position}</dd>
            % endif
        </dl>

    </%util:well>

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

% if len(ctx.analyses) > 1:
    <h3>Analyses</h3>
    <ul>
        % for a in ctx.analyses:
            <li>${a}</li>
        % endfor
    </ul>
% else:
    <div>

        <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'measurements'); dt = dt(request, u.Measurement, analysis=ctx.analyses[0]) %>
        ${dt.render()}
    </div>
% endif
