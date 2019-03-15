<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "unitparameters" %>

<h2>${_('Unit Parameter')} ${ctx.name}</h2>

<div>
    <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'measurements'); dt = dt(request, u.Measurement, unitparameter=ctx) %>
    ${dt.render()}
</div>
