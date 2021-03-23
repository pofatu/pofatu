<%inherit file="../pofatu.mako"/>
<%! multirow = True %>

<div class="row-fluid">

<div class="span3">
    <div class="well" style="margin-top: 1em;">
        <img src="${req.static_url('pofatu:static/logo.png')}">
    </div>
</div>

<div class="span6">
  <h2>Welcome to Pofatu*</h2>
  <small>*Proto Eastern Polynesian for “stone”</small>

<p class="lead">
    An open-access database for geochemical sourcing of archaeological materials.
</p>
<p>
    Geochemical fingerprinting of artefacts and sources has proven to be the most effective way to use material evidence in
    order to reconstruct strategies of raw material procurement, exchange systems, and mobility
    patterns among past societies. In order to facilitate access to this growing body of data and to promote
    comparability and reproducibility in provenance studies, we designed Pofatu, the first online and open-access
    database presenting geochemical compositions and contextual information for archaeological sources and artefacts.
</p>
<p>
    The ${h.external_link('https://github.com/pofatu/pofatu-data', label='data repository')}
    includes a compilation of geochemical data and supporting analytical metadata, as well as the
    archaeological provenance and context for each sample. All information on Samples related to sources and artefacts can
    be accessed on this platform or <a href="${req.route_url('download')}">downloaded from Zenodo or GitHub</a>.
</p>
<p>
    While most prehistoric quarries and surface procurement sources used in the past have yet to be identified,
    provenance studies must also integrate wide and reliable geological data. For this reason, we advise Pofatu users to
    also consult other open-access repositories focusing specifically on geological samples, such as
    ${h.external_link('http://georoc.mpch-mainz.gwdg.de/georoc/', label='GeoRoc')} and
    ${h.external_link('http://www.earthchem.org', label='EarthChem')}.
</p>
</div>
<div class="span3">
    <div class="well well-small" style="margin-top: 1em;">
<a class="twitter-timeline" data-height="400" href="https://twitter.com/pofatu?ref_src=twsrc%5Etfw">Tweets by pofatu</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </div>
</div>


