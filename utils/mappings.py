INCOME_OBJECT_TYPE_MAPPING = {
    'заробітна плата отримана за основним місцем роботи': 'salarymain',
    'заробітна плата отримана за сумісництвом': 'salarysecond',
    'пенсія': 'pension',
    'дохід від надання майна в оренду': 'leasing',
    'дохід від зайняття підприємницькою діяльністю': 'business',
    'гонорари та інші виплати згідно з цивільно-правовим правочинами': 'contractfee',
    'дохід від зайняття незалежною професійною діяльністю': 'indepprof',
    'проценти': 'interest',
    'дивіденди': 'dividends',
    'роялті': 'royalty',
    'страхові виплати': 'insurance',
    'подарунок у негрошовій формі': 'presentnomoney',
    'подарунок у грошовій формі': 'presentmoney',
    'благодійна допомога': 'charity',
    'приз': 'prize',
    'дохід від відчуження нерухомого майна': 'saleestate',
    'дохід від відчуження рухомого майна (крім цінних паперів та корпоративних прав)': 'salemovable',
    'дохід від відчуження цінних паперів та корпоративних прав': 'salestock',
    'спадщина': 'inheritance',
    'інше': 'other'
}

ASSET_OBJECT_TYPE_MAPPING = {
    'кошти, розміщені на банківських рахунках': 'bank',
    'готівкові кошти': 'cash',
    'внески до кредитних спілок та інших небанківських фінансових установ': 'credit_union',
    'кошти, позичені третім особам': 'lend',
    'активи у дорогоцінних (банківських) металах': 'metals',
    'інше': 'other'
}

LIABILITY_OBJECT_TYPE_MAPPING = {
    'зобов\'язання за договорами лізингу': 'leasing',
    'зобов\'язання за договорами недержавного пенсійного забезпечення': 'pension',
    'зобов\'язання за договорами страхування': 'insurance',
    'кошти, позичені суб\'єкту декларування або члену його сім\'ї іншими особами': 'informal_loans',
    'несплачені податкові зобов\'язання': 'taxes',
    'отримані кредити': 'loans_received',
    'отримані позики': 'loans_received',
    'розмір сплачених коштів в рахунок основної суми позики (кредиту)': 'loans_paid',
    'розмір сплачених коштів в рахунок процентів за позикою (кредитом)': 'loans_paid',
    'інше': 'other'
}

ESTATE_OBJECT_TYPE_MAPPING = {
    'квартира': 'apt',
    'земельна ділянка': 'land',
    'житловий будинок': 'house',
    'кімната': 'room',
    'гараж': 'garage',
    'садовий (дачний) будинок': 'dacha',
    'офіс': 'office',
    'інше': 'other'
}

VEHICLE_OBJECT_TYPE_MAPPING = {
    'автомобіль легковий': 'car',
    'сільськогосподарська техніка': 'farm_machinery',
    'автомобіль вантажний': 'truck',
    'мотоцикл (мопед)': 'moto',
    'водний засіб': 'water_transport',
    'повітряний засіб': 'air_transport',
    'інше': 'other'
}

EXPENSE_SPEC_MAPPING = {
    'право власності (у тому числі спільної власності), володіння чи користування суб’єкта декларування припинено': 'property_end',
    'придбання': 'purchase',
    'оренда': 'leasing',
    'суб’єкт декларування набув право власності (у тому числі спільної власності), володіння чи користування': 'property_start',
    'виникло фінансове зобов’язання суб’єкта декларування': 'liability',
    'інше': 'other'
}

PROPERTY_TYPE_MAPPING = {
    'власність': 'ownproperty',
    'спільна власність': 'comproperty',
    'власником є третя особа': 'thirdparty',
    'оренда': 'leasing',
    'інше': 'other'
}

FOREIGN_SOURCE_TAGS = [
    'іноземний громадянин',
    'юридична особа, зареєстрована за кордоном'
]

WORK_ORGANISATION_REGEXPS = [
    ('workPlace', r'судов.*експерт', 'Кабмін, міністерства та підлеглі органи'),
    ('workPost', r'суддя', 'Суд'),
    ('workPost', r'керівник ап{1,2}арат[а|у] суд[а|у]', 'Суд'),
    ('workPlace', r'\sсуд$', 'Суд'),
    ('workPlace', r'\sсуд\s', 'Суд'),
    ('workPost', r'прокурор', 'Прокуратура'),
    ('workPlace', r'прокуратур', 'Прокуратура'),
    ('workPlace', r'адмін.*президента', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'рнбо', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'рад.*нац.*безпек', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'^удо\s', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'^упр.{0,10}держ.{0,8}охор', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'держ.{0,8}упр.{0,10}справ', 'Адміністрація / Секретаріат Президента'),
    ('workPlace', r'верх.{0,7}рад[а|и]', 'Парламент'),
    ('workPlace', r'нац.{0,12}банк', 'НБУ'),
    ('workPlace', r'\sнбу\s', 'НБУ'),
    ('workPlace', r'^нбу$', 'НБУ'),
    ('workPlace', r'\sнбу$', 'НБУ'),
    ('workPlace', r'центр.{0,8}виб.{0,6}коміс', 'ЦВК'),
    ('workPlace', r'(?:обл|рай|міськ).{0,6}держ.{0,6}адмін', 'Місцеві адміністрації та ради'),
    ('workPlace', r'районн(?:а|ої) адмін', 'Місцеві адміністрації та ради'),
    ('workPlace', r'кмда', 'Місцеві адміністрації та ради'),
    ('workPlace', r'обласн(?:а|ої) адмін', 'Місцеві адміністрації та ради'),
    ('workPlace', r'(?:обл|рай).{0,7}рад[а|и]', 'Місцеві адміністрації та ради'),
    ('workPlace', r'рай.{0,6}[у|в] м.{0,6}\s.*\sрада', 'Місцеві адміністрації та ради'),
    ('workPlace', r'рда|\sода', 'Місцеві адміністрації та ради'),
    ('workPlace', r'міськ.{0,4}рад[а|и]', 'Місцеві адміністрації та ради'),
    ('workPlace', r'сіль.{0,7}рад[а|и]', 'Місцеві адміністрації та ради'),
    ('workPlace', r'селищ.{0,5}рад[а|и]', 'Місцеві адміністрації та ради'),
    ('workPlace', r'\sсбу\s', 'СБУ'),
    ('workPlace', r'^сбу$', 'СБУ'),
    ('workPlace', r'\sсбу$', 'СБУ'),
    ('workPlace', r'усбу', 'СБУ'),
    ('workPlace', r'служб[а|и] безпеки укр', 'СБУ'),
    ('workPlace', r'пенс.*фонд', 'Пенсійний фонд'),
    ('workPlace', r'пфу', 'Пенсійний фонд'),
    ('workPlace', r'\sпф\s', 'Пенсійний фонд'),
    ('workPlace', r'^пф\s', 'Пенсійний фонд'),
    ('workPlace', r'\sпф$', 'Пенсійний фонд'),
    ('workPlace', r'фонд.*держ.*майн', 'Фонд державного майна'),
    ('workPlace', r'каб.*мін', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'міністерство', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*агро', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'інсп.*сіль.*госп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'в.т.р.н.* служ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*ліс.*рес', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аге.*риб.*госп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*внутр.*справ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мвс', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'нац.*гвард', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'держ.*служ.{2,4}охор', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'гу\s?нп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'поліц', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'прикордон.*(?:служ|заг)', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'міграц', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'надзвич', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'(?:акад|унів).*внутр.*справ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*природ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'екол.*інсп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'служ.*геол', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*вод.*рес', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*екол.*інвест', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*упр.*зон.*в.{0,3}чу', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'прир.*(?:парк|запов)', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'дфс', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'фіск.*служ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'податк', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*доход', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'одпі', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'митн', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*енерг', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мзс', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*закордон', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'сан.*п.д.м', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'\sмоз\s', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'^моз\s', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'\sмоз$', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'^моз$', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*інфр', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*трансп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'адм.*мор.*порт', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'залізниця', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'авіа*служб', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'без.*(?:мор|назем).*трансп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аген.*туризм', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аген.*авто.*дор', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мінкульт', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'міністер.*культ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аген.*кіно', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'народ.*творч', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'(?:культур|істор).*запов.дник', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'музей', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'(?:худож|музич).*учил', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'учил.*культур', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'б.бл.отек', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'ф.лармон', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'театр', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'оркестр', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*спорт', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*обор', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'ген.*штаб', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'збр.*сил', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*осв.*наук', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'навч.*закл', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'\sмін.*рег', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'^мін.*рег', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*лектрон.*ряд', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*нерго', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*нов.*донбас', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'арх.*буд.*нсп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'служ.*гео.*карт', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'мін.*соц.*пол', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'фонд.*соц.*зах.*інв', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'інсп.*прац', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'служ.*інвал.*ветер', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'фонд.*соц.*страх', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'держ.*служ.*за.?нят', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'\sмін.*фін', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'^мін.*фін', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'\sмін.*юст', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'^мін.*юст', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'управ.*юст', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'пен.т.*служ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'виконав.*служ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'ре.*стра.*служ', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'зах.*персон.*дан', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'держ.*прац', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'вищ.*рад.*(?:юстиц|правосуд)', 'Вища рада юстиції'),
    ('workPlace', r'казнач.*служ', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'упр.*казнач', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'держ.*служ.*стат', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'управ.*стат', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'упр.*статист', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'відділ.*статистик', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'сзр', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'амку|монопол', 'Антимонопольний комітет'),
    ('workPlace', r'ком.*теле', 'Державний комітет телебачення і радіомовлення'),
    ('workPlace', r'інсп.*цін', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'інсп.*спож', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'держ.*спож.*служ', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'вет.*фіто.*служ', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'сан.*епід.*служб', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'інсп.*ядер', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'регулят.*служ', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'експорт.*контр', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'служ.*наркот', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'інт.*влас', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'служ.*ветеран', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'держ.*фін.*інсп', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'гео.*кадас', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'корупц.*бю', 'НАБУ'),
    ('workPlace', r'набу', 'НАБУ'),
    ('workPlace', r'нац*аг*зап*корупц', 'НАЗК'),
    ('workPlace', r'назк', 'НАЗК'),
    ('workPlace', r'фін.*монітор', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'ком.*ц.*п.*фонд', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'нкцпфр', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'дмс', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'центр.*держ.*істор.*архів', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'держ.*арх.в.*служб', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'військ.*частин', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'в/ч', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'дснс', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'служ.*спец.*зв.*зах', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'служ.*посеред.*мир', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'держ.*спец.*зв', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'дксу', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'рахунк.*палат', 'Рахункова палата'),
    ('workPlace', r'дпі', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'аг.*резерв', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'косм.*аген', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'ком.*нерг.*ком.*посл', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'нкрекп', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'ком.*зв.*інф.*зац', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'регул.*ринк.*фін.*посл', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'євро.*12', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'міністер.*економ.*розв', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'безп.*харч.*прод', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'держ.*спец.*служ.*трансп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'служб.*безп.*трансп', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'управ.*ветеринар.*мед', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'\sнп\s', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'держ.*аудит.*служб', 'Інші державні служби, комісії, і т.п.'),
    ('workPlace', r'упр.*прац.*соц.*зах.*нас', 'Місцеві адміністрації та ради'),
    ('workPlace', r'держ.*риб.*аг', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'упр.*охор.*вод.*риб', 'Кабмін, міністерства та підлеглі органи'),
    ('workPlace', r'лісов.*госп', 'Кабмін, міністерства та підлеглі органи'),
]

EMPTY_MARKER = '!немає даних'
