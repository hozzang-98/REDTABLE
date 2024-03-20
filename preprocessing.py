import pandas as pd
from collections import Counter
from project_query import tag_groupby
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import pearsonr

def type_weight(ptm, t_type):

    weight_list = []
    weighted_dic = {'ingredient': 7, 'sauce':5, 'cooking':4, 'option':3}
   
    for i in range(len(ptm)):
        for j in range(weighted_dic[t_type[i]]):
            weight_list.append(ptm[i])

    return weight_list

def product_tag_set(x):

    key_list = []
    label_count_dic = Counter(x)

    for k,v in label_count_dic.items():

        if v > 1:

            key_list.append(k)

    df = tag_groupby(x)
    
    df['tag_set'] = df['tag_set'].apply(lambda x:set(x.split(',')))
    
    for key in key_list:
        ki = label_count_dic[key]-1
        for i in range(label_count_dic[key]-1):
            if len(df[df['product_id'] == key]) != 0:
                tmp = pd.DataFrame([df[df['product_id'] == key].iloc[0]])
                df = pd.concat([df, tmp],axis=0)

    tag_set_list = [df[df['product_id'] == i]['tag_set'].values[0] for i in x]
    tag_set_list = list(map(tuple, tag_set_list))
    
    return tag_set_list

def pearson_sim(input_df, rec_df):
    vectorizer = CountVectorizer(min_df = 1)

    full_text = input_df['ptm_ids'].tolist() + rec_df['ptm_ids'].tolist()
    X = vectorizer.fit_transform(full_text)
    index_list = input_df['product_id'].tolist() + rec_df['product_id'].tolist()

    df = pd.DataFrame(
                            data= X.todense(),
                            index = index_list,
                            columns = vectorizer.get_feature_names_out()
                        )

    input_product = input_df['product_id'][0]
    input_vector = df[df.index==input_product]

    sim_value = []

    for i in range(len(df)):

        iv = input_vector.values[0]
        tv = df.iloc[i].values
        idx_list = []

        for idx, i_t in enumerate(zip(iv,tv)):

            
            # 두 벡터 0인 인 것 제외
            if sum(i_t) != 0: idx_list.append(idx)
        
        fiv, ftv = iv[idx_list], tv[idx_list]
        
        # 벡터 최소 길이 2 이상
        if len(fiv) <= 1:
            pearson_similarity = 0
        else:
            pearson_similarity = pearsonr(fiv, ftv)[0]
            
        sim_value.append(round(pearson_similarity,2))

    df['CB 유사도'] =  sim_value
    df.fillna(0,inplace=True)
    result = df[['CB 유사도']]
    result = result.reset_index().rename(columns={'index':'product_id'})
    result.sort_values(by='CB 유사도',ascending=False, inplace=True)
    result.reset_index(inplace=True)
    result.drop('index',axis=1,inplace=True)

    return result