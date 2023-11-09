<%inherit file="../home_comp.mako"/>

<div style="float: left; width: 20%; margin-right: 20px; margin-top: 1em;">
    <img src="${req.static_url('pofatu:static/logo.png')}">
</div>

<h2>Welcome to Pofatu*</h2>
<small>*Proto Eastern Polynesian for “stone”</small>

<p class="lead">
    An open-access database for geochemical sourcing of archaeological materials.
</p>
<p>
    Geochemical fingerprinting of artefacts and sources is an effective way to use material evidence in order to
    reconstruct strategies of raw material procurement, exchange systems, and mobility patterns among past societies. In
    order to facilitate access to this growing body of data and to promote comparability and reproducibility in
    provenance studies, we designed Pofatu, the first online and open-access database presenting geochemical
    compositions and contextual information for archaeological sources and artefacts.
    The
    ${h.external_link('https://github.com/pofatu/pofatu-data', label='data repository')}
    includes a compilation of geochemical data and
    supporting analytical metadata, as well as the archaeological provenance and context for each sample. Information
    related to sources and artefacts can be accessed on this platform and
    <a href="${req.route_url('download')}">downloaded from Zenodo or GitHub</a>.
</p>


<div style="float: right; width: 40%;">
    <figure>
        <img src="${req.static_url('pofatu:static/shrine.jpg')}" class="img-polaroid">
        <figcaption>
            Two huge piles of dark stone flakes, associated with a shrine in background, resulting from the
            manufacture of stone adzes at the high-altitude quarry at Mauna Kea, Hawai'i. (Photo credit: Marshall
            Weisler)
        </figcaption>
    </figure>
</div>


<p class="lead">
    Geochemical sourcing and long-distance voyaging among Pacific Island societies.
</p>
<p>
    Archaeologists use provenance studies to uncover the origin and the life-history of artefacts, including those that
    are sometimes found very far away from their source or place of manufacture. To this end, reliable archaeometric
    data facilitates the reconstruction of technological, economic, and social behaviours of human societies over many
    thousands of years. In the Pacific region, geochemical sourcing has been particularly successful at locating sources
    of stone artefacts among the thousands of islands in the Pacific Ocean.
</p>
<p>
    Provenance studies are also instrumental in showing how specific high-quality resources, extracted and transformed
    in large scale quarries and workshops such as Mauna Kea on Hawai'i Island, Tataga Matau on Tutuila Island (American
    Sāmoa), or the ‘quarry-island’ of Eiao Island in the northern Marquesas (French Polynesia), were distributed among
    neighbouring communities and through long-distance interisland exchange networks. The discovery of these tools far
    from their places of origin
    ${h.external_link('https://www.pnas.org/content/113/29/8150', label='indicate long-term inter-archipelago interactions')},
    as well as wealth economies and extensive political alliances in the highly hierarchical chiefdoms of
    ${h.external_link('https://www.pnas.org/content/109/4/1056', label="Hawai'i")},
    ${h.external_link('https://www.pnas.org/content/111/29/10491', label="Tonga")},
    and the
    ${h.external_link('https://onlinelibrary.wiley.com/doi/full/10.1002/arco.5187', label="Society Islands")}.
    Such material evidence of long-distance inter-island
    voyaging shows that Pacific island societies were never completely isolated from one another, and these patterns of
    interaction are central to our understanding of the deeply intertwined historical trajectories of Pacific Island
    societies.
</p>

<div style="float: left; width: 40%;">
    <figure>
        <img src="${req.static_url('pofatu:static/tupuai.jpg')}" class="img-polaroid">
        <figcaption>
            Archaeological mapping and excavations at the entrance of the Tanataetea quarry in Tupua'i, Austral
            Islands. (Photo credit: Aymeric Hermann)_
        </figcaption>
    </figure>
</div>


<p class="lead">
    Open data for a collective, collaborative, and open science.
</p>
<p>
    Pofatu is the first
    <emph>open-access</emph>
    database of geochemical compositions and contextual information for archaeological
    sources and artefacts in a form readily accessible to the scientific community. As such, Pofatu is an operational
    framework that enables data curation and data sharing in archaeometry, following the
    ${h.external_link('https://www.nature.com/articles/sdata201618', label="FAIR principles")}.
    Additionally, the database provides comprehensive methodological
    metadata (instrumental details, analytical procedures and reference standards used for calibration purposes and
    quality control) and therefore ensure reproducibility and comparability between provenance studies. Because it is
    open access, enables reproducibility, and facilitates reuse of existing data, Pofatu will be useful for crediting
    previous work while advancing future studies in archaeological sciences.
    The database uses GitHub for collaborative, versioned data curation and common non-proprietary file formats (CSV)
    to enable transparency and built-in reproducibility for future studies of prehistoric exchange.
    The quality control of each new dataset consists in a
    <emph>peer review</emph>
    process that includes qualitative and
    quantitative data review and users feedback.
</p>


<div style="float: right; width: 40%;">
    <figure>
        <img src="${req.static_url('pofatu:static/glistening.jpg')}" class="img-polaroid">
        <figcaption>
            Stone flakes glistening in the sun on Eiao the ‘quarry-island’, Henua 'Enana, Marquesas Islands
            (Photo credit: Jean-François Butaud)_
        </figcaption>
    </figure>
</div>


<p class="lead">
    A tool for interdisciplinary research.
</p>
<p>
    Since most prehistoric quarries and surface procurement sources used in the past have yet to be identified,
    provenance studies in archaeology must also integrate wide and reliable geological data. For this reason, we advise
    Pofatu users to also consult other open-access repositories focusing specifically on geological samples, such as
    ${h.external_link('http://georoc.mpch-mainz.gwdg.de/georoc/', label="GeoRoc")} and
    ${h.external_link('http://www.earthchem.org/', label="EarthChem")}.
    Simultaneously, the Pofatu Database can be used by geologists as a complementary source of information because it
    contains geographical and geochemical data on geological outcrops, secondary deposits and raw materials extracted in
    prehistoric quarries from some of the most remote and isolated places on the planet. In that sense, Pofatu is a tool
    that will also facilitate interdisciplinary research as part of a growing geoinformatics network.
</p>

<table>
    <tr>
        <td>
            <img width="100" src="${req.static_url('pofatu:static/cnrs_logo.png')}" style="margin-right: 30px;">
        </td>
        <td>
            <p class="lead">
                Acknowledgements
            </p>
            <p>
                Work on Pofatu is supported by
                ${h.external_link('http://www.cnrs.fr/', label="CNRS")} and
                ${h.external_link('https://www.mpg.de/de', label="Max-Planck-Gesellschaft")}.
            </p>
        </td>
        <td>
            <img width="100" src="${req.static_url('clldmpg:static/minerva.png')}" style="margin-left: 30px;">
        </td>
    </tr>
</table>
