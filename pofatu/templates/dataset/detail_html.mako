<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <img src="${req.static_url('pofatu:static/POFATU.png')}">
    </div>
</%def>

<h2>Welcome to POFATU</h2>

<p class="lead">
    An open-access database for provenance analysis of stone tools in the Pacific.
</p>
<p>
    <i>Pofatu</i> is the proto-Polynesian word for stone. This database is the first online
    and open-access collection of published geochemical data on stone artefacts and quarries
    in the Pacific. The data repository includes metadata about archaeological and chronological
    contexts as well as geographical locations, which can be used to document and quantify
    patterns of change in stone material distribution among Pacific societies through time.
</p>
<p>
    While most prehistoric quarries and surface procurement sources have yet to be identified,
    provenance studies must also rely on the acquisition of wide and reliable geological data.
    For this reason, <i>Pofatu</i> additionally provides a direct access to the geological data
    available from the ${h.external_link('http://georoc.mpch-mainz.gwdg.de/', label='GEOROC')} database.
</p>
