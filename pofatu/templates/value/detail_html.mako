<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<%def name="sidebar()">
    <div class="accordion" id="sidebar-accordion" style="margin-top: 1em; clear: right;">
    <%util:accordion_group eid="acc-location" parent="sidebar-accordion" title="Location" open="${True}">
        <p>${h.link(request, ctx.valueset.language)}</p>
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
        </dl>
    </%util:accordion_group>
    <%util:accordion_group eid="acc-artefact" parent="sidebar-accordion" title="Artefact">
        <dl>
            <dt>Name</dt>
            <dd>${ctx.artefact_name}</dd>
            % if ctx.artefact_category:
                <dt>Category</dt>
                <dd>${ctx.artefact_category}</dd>
            % endif
            <dt>References</dt>
            <dd>
                <ul class="unstyled">
                    % for src in ctx.source_dict.get('artefact', []):
                        <li>${h.link(req, src)}</li>
                    % endfor
                </ul>
            </dd>
        </dl>
    </%util:accordion_group>
    <%util:accordion_group eid="acc-site" parent="sidebar-accordion" title="Site">
        <dl>
            % if ctx.site_name:
                <dt>Name</dt>
                <dd>${ctx.site_name}</dd>
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
            <dt>References</dt>
            <dd>
                <ul class="unstyled">
                    % for src in ctx.source_dict.get('site', []):
                        <li>${h.link(req, src)}</li>
                    % endfor
                </ul>
            </dd>
        </dl>
    </%util:accordion_group>
</%def>


    <h2>${ctx.domainelement.name.capitalize()} ${ctx.name}</h2>

    From reference ${h.link(req, ctx.source_dict['sample'][0])} in contribution ${h.link(req, ctx.valueset.contribution)}.

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
