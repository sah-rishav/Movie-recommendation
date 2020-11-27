def index():

    import pandas as pd
def load_recommendations(): 
    item_similarity_df = pd.read_csv("applications/movies/static/item_similarity_df.csv",index_col=0)
    print("item_similarity_df cached in memory")
    return item_similarity_df 

item_similarity_df = cache.ram('item_similarity_df3',load_recommendations,None) 
print(item_similarity_df.head())

def check_seen(recommended_movie,watched_movies):
    for movie_id,movie in watched_movies.items():
        if recommended_movie == movie["title"]:
            return True
    return False

def get_similar_movies(movie_name,user_rating):
    try:
        similar_score = item_similarity_df[movie_name]*(user_rating-2.5)
        similar_score = similar_score.sort_values(ascending=False)
    except:
        print("don't have movie in model")
        similar_score = pd.Series([])
    
    return similar_score


@service.json
def get_recommendations(watched_movies):

    print(watched_movies)
    similar_movies = pd.DataFrame()

    for movie_id,movie in watched_movies.items():
        similar_movies = similar_movies.append(get_similar_movies(movie["title"],movie["rating"]),ignore_index=True)

    all_recommend = similar_movies.sum().sort_values(ascending=False)

    recommended_movies = []
    for movie,score in all_recommend.iteritems():
        if not check_seen(movie,watched_movies):
            recommended_movies.append(movie)    

    if len(recommended_movies) > 100:
        recommended_movies = recommended_movies[0:100]        

    return recommended_movies
