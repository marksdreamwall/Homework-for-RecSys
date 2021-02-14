def prefilter_items(data_train, ids_by_departments, N_weeks=52, N_top=50, N_bot=50, N_top_cost=10, N_bot_cost=30):
    # Оставим только 5000 самых популярных товаров
    popularity = data_train.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top_5000 = popularity.sort_values('n_sold', ascending=False).head(5000).item_id.tolist()
    #добавим, чтобы не потерять юзеров
    data_train.loc[~data_train['item_id'].isin(top_5000), 'item_id'] = 999999 
        
    # Уберем самые популярные 
    first = top_5000[:N_top] # выбираем топ 50 популярных товаров
    data_train = data_train.loc[~data_train['item_id'].isin(first)]
    
    # Уберем самые непопулряные 
    last = top_5000[len(top_5000) - N_bot:] # выбираем 50 не популярных товаров
    data_train = data_train.loc[~data_train['item_id'].isin(last)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    data_train = data_train[data_train.week_no > (data_train['week_no'].max() - N_weeks)]
    
    # Уберем не интересные для рекоммендаций категории (department)
    data_train = data_train.loc[~data_train['item_id'].isin(ids_by_departments)]
    
    # Расчеты стоимостей товаров
    quanti = data_train.groupby('item_id')['quantity'].sum().reset_index()
    cost = data_train.groupby('item_id')['sales_value'].sum().reset_index()
    cost['devide'] = cost.sales_value/quanti.quantity
    cost = cost[cost.devide != np.inf] # уберем inf
    cost = cost.fillna(0) # заполним NaN's
    
    # стоимость более 300 (долларов?)
    expensive = cost.loc[cost.devide > 300].sort_values('devide', ascending=False).item_id.to_list()
    # стоимость менеее 1 доллара
    less_1 = cost.loc[cost.devide > 1].sort_values('devide', ascending=False).item_id.to_list()
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    data_train = data_train.loc[~data['item_id'].isin(less_1)]
    
    # Уберем слишком дорогие товары
    data_train = data_train.loc[~data['item_id'].isin(expensive)]

    return data_train

def postfilter_items():
    pass