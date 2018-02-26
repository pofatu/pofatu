<%inherit file="app.mako"/>

<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">
        <img src="${req.static_url('pofatu:static/logo.png')}" height="20" width="20" style="margin-top: -5px; margin-left: -20px;"/>
        ${request.dataset.name}
    </a>
</%block>

${next.body()}
