(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_1)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    const full_name = `${doc.step_1.lastname} ${doc.step_1.firstname} ${doc.step_1.middlename}`;
    emit(doc._id,
         [full_name, doc.step_1.workPost, doc.step_1.workPlace, doc.step_0.declarationYear1]);
}