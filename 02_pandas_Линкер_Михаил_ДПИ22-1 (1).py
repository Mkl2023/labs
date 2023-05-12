#!/usr/bin/env python
# coding: utf-8

# # Pandas

# Материалы:
# * Макрушин С.В. "Лекция 2: Библиотека Pandas"
# * https://pandas.pydata.org/docs/user_guide/index.html#
# * https://pandas.pydata.org/docs/reference/index.html
# * Уэс Маккини. Python и анализ данных

# ## Задачи для совместного разбора

# 1. Загрузите данные из файла `sp500hst.txt` и обозначьте столбцы в соответствии с содержимым: `"date", "ticker", "open", "high", "low", "close", "volume"`.

# 2. Рассчитайте среднее значение показателей для каждого из столбцов c номерами 3-6.

# 3. Добавьте столбец, содержащий только число месяца, к которому относится дата.

# 4. Рассчитайте суммарный объем торгов для для одинаковых значений тикеров.

# 5. Загрузите данные из файла sp500hst.txt и обозначьте столбцы в соответствии с содержимым: "date", "ticker", "open", "high", "low", "close", "volume". Добавьте столбец с расшифровкой названия тикера, используя данные из файла `sp_data2.csv` . В случае нехватки данных об именах тикеров корректно обработать их.

# ## Лабораторная работа №2

# ### Базовые операции с `DataFrame`

# 1.1 В файлах `recipes_sample.csv` и `reviews_sample.csv` находится информация об рецептах блюд и отзывах на эти рецепты соответственно. Загрузите данные из файлов в виде `pd.DataFrame` с названиями `recipes` и `reviews`. Обратите внимание на корректное считывание столбца с индексами в таблице `reviews` (безымянный столбец).

# In[67]:


import pandas as pd


# In[68]:


recipes = pd.read_csv("recipes_sample.csv")
reviews = pd.read_csv("reviews_sample.csv", index_col = 0)
reviews


# 1.2 Для каждой из таблиц выведите основные параметры:
# * количество точек данных (строк);
# * количество столбцов;
# * тип данных каждого столбца.

# In[27]:


print("\n'recipes':\n\nкол-во строк:", recipes.shape[0], "\n", "кол-во столбцов:", recipes.shape[1], "\n", "тип данных:\n", recipes.dtypes, sep="")
print("\n'reviews':\n\nкол-во строк:", reviews.shape[0], "\n", "кол-во столбцов:", reviews.shape[1], "\n", "тип данных:\n", reviews.dtypes, sep="")


# 1.3 Исследуйте, в каких столбцах таблиц содержатся пропуски. Посчитайте долю строк, содержащих пропуски, в отношении к общему количеству строк.

# In[47]:


print("recipes:")
print(recipes.isna().sum())
print(recipes.isna().sum() / len(reviews))
print("\nreviews:")
print(reviews.isna().sum())
print(reviews.isna().sum() / len(reviews))


# 1.4 Рассчитайте среднее значение для каждого из числовых столбцов (где это имеет смысл).

# In[50]:


recipes.mean(axis=0)


# 1.5 Создайте серию из 10 случайных названий рецептов.

# In[4]:


recipes["name"].sample(10)


# 1.6 Измените индекс в таблице `reviews`, пронумеровав строки, начиная с нуля.

# In[5]:


reviews = reviews.reset_index(drop=True)
reviews


# 1.7 Выведите информацию о рецептах, время выполнения которых не больше 20 минут и кол-во ингредиентов в которых не больше 5.

# In[4]:


recipes.loc[(recipes["minutes"] <= 20) & (recipes["n_ingredients"] <= 5)]


# ### Работа с датами в `pandas`

# 2.1 Преобразуйте столбец `submitted` из таблицы `recipes` в формат времени. Модифицируйте решение задачи 1.1 так, чтобы считать столбец сразу в нужном формате.

# In[70]:


recipes['submitted'] = pd.to_datetime(recipes['submitted'])


# 2.2 Выведите информацию о рецептах, добавленных в датасет не позже 2010 года.

# In[71]:


new_rec = recipes[recipes['submitted'].dt.year >= 2010]
new_rec


# ### Работа со строковыми данными в `pandas`

# 3.1  Добавьте в таблицу `recipes` столбец `description_length`, в котором хранится длина описания рецепта из столбца `description`.

# In[72]:


recipes = recipes.astype({'description' : 'string'})
recipes['description_length'] = recipes['description'].str.len()
recipes


# 3.2 Измените название каждого рецепта в таблице `recipes` таким образом, чтобы каждое слово в названии начиналось с прописной буквы.

# In[73]:


recipes['name'] = recipes['name'].str.capitalize()
recipes


# 3.3 Добавьте в таблицу `recipes` столбец `name_word_count`, в котором хранится количество слов из названии рецепта (считайте, что слова в названии разделяются только пробелами). Обратите внимание, что между словами может располагаться несколько пробелов подряд.

# In[74]:


recipes['name_word_count'] = recipes['name'].str.split().str.len()
recipes


# ### Группировки таблиц `pd.DataFrame`

# 4.1 Посчитайте количество рецептов, представленных каждым из участников (`contributor_id`). Какой участник добавил максимальное кол-во рецептов?

# In[75]:


print(recipes.groupby('contributor_id')['id'].count())
print("\nучастник", recipes.groupby('contributor_id')['id'].count().idxmax(), "добавил максимальное кол-во рецептов")


# 4.2 Посчитайте средний рейтинг к каждому из рецептов. Для скольких рецептов отсутствуют отзывы? Обратите внимание, что отзыв с нулевым рейтингом или не заполненным текстовым описанием не считается отсутствующим.

# In[76]:


print(reviews.groupby('recipe_id')['rating'].mean())
print("\nОтзывы отсутствуют для", len(recipes[~recipes['id'].isin(reviews['recipe_id'])]), "рецептов")


# 4.3 Посчитайте количество рецептов с разбивкой по годам создания.

# In[77]:


#r_b_y = recipes.groupby(pd.Grouper(key="submitted", freq="Y")).count()['id']
#r_b_y.index = r_b_y.index.year
#r_b_y

print(recipes[['id', 'submitted']].groupby('submitted').count())


# ### Объединение таблиц `pd.DataFrame`

# 5.1 При помощи объединения таблиц, создайте `DataFrame`, состоящий из четырех столбцов: `id`, `name`, `user_id`, `rating`. Рецепты, на которые не оставлен ни один отзыв, должны отсутствовать в полученной таблице. Подтвердите правильность работы вашего кода, выбрав рецепт, не имеющий отзывов, и попытавшись найти строку, соответствующую этому рецепту, в полученном `DataFrame`.

# In[92]:


recipes_with_rating = pd.merge(recipes[['id', 'name']], 
                               reviews[['recipe_id', 'user_id', 'rating']], 
                               left_on='id', 
                               right_on='recipe_id').drop('recipe_id', axis=1)
print(recipes_with_rating, "\n")

no_reviews = recipes[~recipes['id'].isin(reviews['recipe_id'])]

recipe_without_rating = no_reviews.sample()
print(recipe_without_rating.isin(recipes_with_rating)['name'])


# 5.2 При помощи объединения таблиц и группировок, создайте `DataFrame`, состоящий из трех столбцов: `recipe_id`, `name`, `review_count`, где столбец `review_count` содержит кол-во отзывов, оставленных на рецепт `recipe_id`. У рецептов, на которые не оставлен ни один отзыв, в столбце `review_count` должен быть указан 0. Подтвердите правильность работы вашего кода, выбрав рецепт, не имеющий отзывов, и найдя строку, соответствующую этому рецепту, в полученном `DataFrame`.

# In[93]:


new_recipes = recipes.rename(columns={'id': 'recipe_id'})
review_count = reviews.groupby('recipe_id', as_index=False)['review'].count()
recipes_reviews = pd.merge(new_recipes[['recipe_id', 'name']], review_count, how='left').fillna(0)

recipes_reviews = recipes_reviews.rename(columns={'review': 'review_count'})
print(recipes_reviews, "\n")

no_reviews1 = new_recipes[~new_recipes['recipe_id'].isin(reviews['recipe_id'])]

recipe_without_reviews = no_reviews1.sample()
print(recipe_without_reviews.isin(recipes_reviews)['recipe_id'])


# 5.3. Выясните, рецепты, добавленные в каком году, имеют наименьший средний рейтинг?

# In[80]:


general_df = recipes.copy().drop(columns = ['name', 'minutes', 'contributor_id', 'description', 'n_ingredients', 'description_length', 'name_word_count', 'n_steps'])
general_df['year'] = general_df['submitted'].dt.year
general_df = general_df.reindex(columns=['id', 'year'])
average_rate = reviews.groupby('recipe_id')['rating'].mean()
general_df = pd.merge(general_df.set_index('id'), average_rate, how='left', left_index=True, right_index=True)
general_df['id'] = general_df.index
general_df['rating'] = general_df['rating'].fillna(0)
year_rate = general_df.groupby('year')['rating'].mean()
minrate_year = year_rate[year_rate == year_rate.min()].index[0]
print('Min average rating year is {0} and rating was = {1}'.format(minrate_year, year_rate.min()))


# ### Сохранение таблиц `pd.DataFrame`

# 6.1 Отсортируйте таблицу в порядке убывания величины столбца `name_word_count` и сохраните результаты выполнения заданий 3.1-3.3 в csv файл. 

# In[85]:


recipes = recipes.sort_values(by=['name_word_count'], ascending=False)
display(recipes)
recipes.to_csv('recipes_result.csv', sep=',')


# 6.2 Воспользовавшись `pd.ExcelWriter`, cохраните результаты 5.1 и 5.2 в файл: на лист с названием `Рецепты с оценками` сохраните результаты выполнения 5.1; на лист с названием `Количество отзывов по рецептам` сохраните результаты выполнения 5.2.

# In[97]:


with pd.ExcelWriter('new_datasets.xlsx') as writer:
    recipe_without_rating.to_excel(writer, sheet_name='Рецепты с оценками', index=False)
    recipe_without_reviews.to_excel(writer, sheet_name='Количество отзывов по рецептам', index=False)
    writer.save()


# #### [версия 2]
# * Уточнены формулировки задач 1.1, 3.3, 4.2, 5.1, 5.2, 5.3

# In[ ]:




