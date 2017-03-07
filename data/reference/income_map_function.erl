fun({Doc}) ->
    {Step0} = proplists:get_value(<<"step_0">>, Doc, {nil}),
    {Step1} = proplists:get_value(<<"step_1">>, Doc, {nil}),
    % This is ugly but sometimes "step_11" exists but is not an object, thus needs this "unboxing"
    Step11 = case proplists:get_value(<<"step_11">>, Doc, nil) of
        {Val} -> Val;
        NotObject -> NotObject
    end,

    Calc_income = fun(Value, Acc) ->
        case Value of
            {Key, {IncomeDoc}} ->
                {DeclarantSalarySum, FamilySalarySum, DeclarantTotalSum, FamilyTotalSum} = Acc,
                IsSalary = proplists:get_value(<<"objectType">>, IncomeDoc) =:= <<"Заробітна плата отримана за основним місцем роботи">>,
                Size = proplists:get_value(<<"sizeIncome">>, IncomeDoc),
                case proplists:get_value(<<"person">>, IncomeDoc) of
                    <<"1">> ->
                        if
                            IsSalary -> {DeclarantSalarySum + Size, FamilySalarySum, DeclarantTotalSum + Size, FamilyTotalSum};
                            true -> {DeclarantSalarySum, FamilySalarySum, DeclarantTotalSum + Size, FamilyTotalSum}
                        end;
                    _ ->
                        if
                            IsSalary -> {DeclarantSalarySum, FamilySalarySum + Size, DeclarantTotalSum, FamilyTotalSum + Size};
                            true -> {DeclarantSalarySum, FamilySalarySum, DeclarantTotalSum, FamilyTotalSum + Size}
                        end
                end;
            _ -> Acc
        end
    end,

    if
        Step0 =/= nil andalso Step1 =/= nil ->
            case proplists:get_value(<<"declarationType">>, Step0, nil) of
                <<"1">> ->
                    {DeclarantSalarySum, FamilySalarySum, DeclarantTotalSum, FamilyTotalSum} = case Step11 of
                        nil -> {0, 0, 0, 0};
                        _ -> lists:foldl(Calc_income, {0, 0, 0, 0}, Step11)
                    end,
                    Id = proplists:get_value(<<"_id">>, Doc),
                    Lastname = proplists:get_value(<<"lastname">>, Step1),
                    Firstname = proplists:get_value(<<"firstname">>, Step1),
                    Middlename = proplists:get_value(<<"middlename">>, Step1),
                    Result = {[
                        {<<"FIO">>, <<Lastname/binary, " ", Firstname/binary, " ", Middlename/binary>>},
                        {<<"workPost">>, proplists:get_value(<<"workPost">>, Step1, nil)},
                        {<<"workPlace">>, proplists:get_value(<<"workPlace">>, Step1, nil)},
                        {<<"decl_year">>, proplists:get_value(<<"declarationYear1">>, Step0, nil)},
                        {<<"salary_declarant_sum">>, DeclarantSalarySum},
                        {<<"salary_family_sum">>, FamilySalarySum},
                        {<<"total_income_declarant">>, DeclarantTotalSum},
                        {<<"total_income_family">>, FamilyTotalSum}
                    ]},
                    Emit(Id, Result);
                _ ->
                    nil
            end;
        true ->
            nil
    end
end.
