(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_1)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    const dcu_link = `https://declarations.com.ua/declaration/${doc._id}`,
          full_name = `${doc.step_1.lastname} ${doc.step_1.firstname} ${doc.step_1.middlename}`,
          name_post = `${full_name}, ${doc.step_1.workPost}, ${doc.step_1.workPlace}`,
          has_family = typeof(doc.step_2) == 'object' && !Array.isArray(doc.step_2);
    emit(doc._id,
         [dcu_link, full_name, doc.step_1.workPost, doc.step_1.workPlace, doc.step_0.declarationYear1, name_post,
          has_family, doc.step_1.organization_group, doc.mapped_region]);
}