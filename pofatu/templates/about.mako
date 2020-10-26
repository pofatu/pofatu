<%inherit file="home_comp.mako"/>

<h3>How to cite Pofatu</h3>

<p>
    To cite the database, please cite
</p>

<blockquote>
    Aymeric Hermann & Robert Forkel. (2020). pofatu/pofatu-data: Pofatu, a curated and open-access database for geochemical sourcing of archaeological materials (Version v1.1.1) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4134337
    <br/>
    <a href="https://doi.org/10.5281/zenodo.4134337"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4134337.svg" alt="DOI"></a>
</blockquote>
<p>
    as well as our paper introducing the database
</p>
<blockquote>
    Hermann, A., Forkel, R., McAlister, A. et al. Pofatu, a curated and open-access database for geochemical sourcing of archaeological materials. Sci Data 7, 141 (2020). <a href="https://doi.org/10.1038/s41597-020-0485-8">DOI: 10.1038/s41597-020-0485-8</a>
</blockquote>

<p>
    Please also acknowledge the original scientists who contributed to the downloaded dataset by appropriately crediting the original data sources. We strongly encourage the publication of a secondary bibliography, which can be submitted as a supplementary material file.
</p>

<h3>How to contribute</h3>
<p>
    We welcome all contributions of geochemical data on archaeological material, regardless of geographic or chrono-cultural boundaries.
    In order to contribute data, please download and use our
    ${h.external_link('https://github.com/pofatu/pofatu-data/blob/master/doc/Pofatu%20Data%20Submission%20Template.xlsx?raw=true', label='Data Submission Template')}
    and
    ${h.external_link('https://github.com/pofatu/pofatu-data/blob/master/doc/Pofatu%20Data%20Submission%20Guidelines.pdf?raw=true', label='Guidelines')}.
</p>


<h3>Contact us</h3>
<p>
    You can contact us via email at: ${req.dataset.contact}
</p>
