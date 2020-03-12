(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || !nacp_doc.step_1)
        return;

    const dcu_link = `https://declarations.com.ua/declaration/${doc.doc_uuid}`,
          full_name = `${nacp_doc.step_1.lastname} ${nacp_doc.step_1.firstname} ${nacp_doc.step_1.middlename}`,
          work_post = nacp_doc.step_1.workPost || "",
          work_place = nacp_doc.step_1.workPlace || "",
          corruption_affected = nacp_doc.step_1.corruptionAffected || "",
          post_category = nacp_doc.step_1.postCategory || "",
          post_category_extendedstatus = nacp_doc.step_1.postCategory_extendedstatus || "",
          post_type = nacp_doc.step_1.postType || "",
          public_person = nacp_doc.step_1.public_person || "",
          responsible_position = nacp_doc.step_1.responsiblePosition || "";

    let has_family = false,
        name_post = full_name;

    if (work_post)
      name_post += ", " + work_post

    if (work_place)
      name_post += ", " + work_place

    if (!nacp_doc.step_0.changesYear && nacp_doc.step_0.declarationType) {
      has_family = typeof(nacp_doc.step_2) == 'object';
    }


    // Quick fix to have a little less categories
    let mapped_region = doc.general.post.actual_region;
    if (mapped_region == 'Севастополь')
        mapped_region = 'Кримська Автономна Республіка';
    emit(doc._id,
         [doc.doc_uuid, dcu_link, full_name, nacp_doc.step_0.declarationYear1, name_post,
          has_family, nacp_doc.step_1.dnt_organization_group, mapped_region, doc.intro.user_declarant_id,
          corruption_affected, post_category, post_category_extendedstatus, post_type,
          public_person, responsible_position, doc.intro.date, doc.intro.doc_type]);
}