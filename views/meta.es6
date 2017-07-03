(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType || !nacp_doc.step_1)
        return;
    if (nacp_doc.step_0.declarationType != '1')
        return;

    const dcu_link = `https://declarations.com.ua/declaration/${doc.doc_uuid}`,
          full_name = `${nacp_doc.step_1.lastname} ${nacp_doc.step_1.firstname} ${nacp_doc.step_1.middlename}`,
          name_post = `${full_name}, ${nacp_doc.step_1.workPost}, ${nacp_doc.step_1.workPlace}`,
          has_family = typeof(nacp_doc.step_2) == 'object';
    // Quick fix to have a little less categories
    let mapped_region = doc.general.post.region;
    if (mapped_region == 'Севастополь')
        mapped_region = 'Кримська Автономна Республіка';
    emit(doc._id,
         [dcu_link, full_name, nacp_doc.step_0.declarationYear1, name_post,
          has_family, nacp_doc.step_1.organization_group, mapped_region]);
}