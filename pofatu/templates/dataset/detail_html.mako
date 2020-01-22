<%inherit file="../pofatu.mako"/>

<%def name="sidebar()">
    <div class="well">
        <img src="${req.static_url('pofatu:static/logo.png')}">
    </div>
</%def>


<h2>Welcome to Pofatu*</h2>
<small>*Proto-Polynesian for “stone”</small>

<p class="lead">
    An open-access database for geochemical sourcing of archaeological materials.
</p>
<p>
    Geochemical fingerprinting artefacts and sources has proven to be the most effective way to use material evidence in
    order to reconstruct raw material procurement practices, intra- and inter-community interactions, and mobility
    patterns among past societies. In order to facilitate access to this growing body of data and to promote
    comparability and reproducibility in provenance studies, we designed Pofatu, the first online and open-access
    database presenting geochemical compositions and contextual information for archaeological sources and artefacts.
</p>
<p>
    The data repository includes a compilation of geochemical data and supporting analytical metadata, as well as the
    archaeological provenance and context for each sample. All information Samples related to sources and artefacts can
    be accessed on this platform or downloaded there.
</p>
<p>
    While most prehistoric quarries and surface procurement sources used in the past have yet to be identified,
    provenance studies must also rely on wide and reliable geological data. For this reason, we advise Pofatu users to
    also consult other open-access repositories focusing specifically on geological samples, such as
    ${h.external_link('http://georoc.mpch-mainz.gwdg.de/georoc/', label='GeoRoc')} and
    ${h.external_link('http://www.earthchem.org', label='EarthChem')}.
</p>
