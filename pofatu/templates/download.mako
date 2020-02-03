<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>


<h3>Downloads</h3>

<div class="alert alert-info">
    <p>
        Pofatu serves the latest
        ${h.external_link('https://github.com/pofatu/pofatu-data/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/pofatu/pofatu-data', label='pofatu/pofatu-data')}.
        All released versions are accessible via <br/>
        <a href="https://doi.org/10.5281/zenodo.3634435"><img
                src="https://zenodo.org/badge/DOI/10.5281/zenodo.3634435.svg" alt="DOI"></a>
        <br/>
        on ZENODO as well.
    </p>
</div>
