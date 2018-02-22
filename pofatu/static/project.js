DPLACE2 = {};

CLLD.MapIcons.div = function (feature, size, url) {
    var c = 'pofatu-map-icon';
    if (feature.properties.type == 'ARTEFACT') {
        c += ' pofatu-map-icon-artefact';
    }
    return L.divIcon({
        //html: '<div class="dplace-map-icon" style="background: ' + feature.properties.color + ';">☺</div>',
        html: '<div class="' + c + '" style="background: ' + feature.properties.color + ';">&nbsp;</div>',
        className: 'clld-map-icon'
    });
};
