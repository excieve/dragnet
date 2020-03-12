// Even more Danger Zoooone
(doc) => {
	function parse_date(dt) {
		return Date.parse(dt.split(".").reverse().join("-"))
	}

    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || !nacp_doc.step_0.changesYear)
        return;

    let untimely_submission = false;
    const created_date = Date.parse(doc.intro.date);

    function drilldown(obj) {
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                if (i == "step_1") {
                    continue;
                }

                if (typeof obj[i] === 'object') {
                    var violation_found = drilldown(obj[i]);
                    if (violation_found) {
                        return violation_found;
                    }
                } else if (String(i).toLowerCase() == "owningdate") {
                	if (created_date - parse_date(obj[i]) >= 10 * 24 * 60 * 60 * 1000) {
                		return true;
                	}
                }
            }
        }
        return false;
    };

    untimely_submission = drilldown(nacp_doc)

    emit(doc._id, [doc.doc_uuid, untimely_submission]);
}
