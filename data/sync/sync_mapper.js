(function () {
    var mapId = function (doc) {
        doc['_id'] = doc['doc_uuid'];
        return doc;
    };

    module.exports = function (doc) {
        return doc['_id'].startsWith('_design/') ? null : mapId(doc);
    }
})();
