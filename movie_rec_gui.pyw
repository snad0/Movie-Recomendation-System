import numpy as np
import pandas as pd
import difflib #to get the closest match
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sklearn.utils._typedefs
from tkinter import *
root =Tk()

root.geometry("720x520")
root.config(bg='black')
root.title("Movie Recomendation System")
bg= PhotoImage(file='12.png')
label =Label(root, image=bg)
label.place(x=0, y=0)
lbox=Listbox(root)

    
def getval():
    movie_name = movie_name1.get()
    #Creating a list with all the movie name given in the data set
    List_of_all_titles = movies_data['title'].tolist()

    #finding the close match for the movie name given by the user 
    Find_close_match = difflib.get_close_matches(movie_name, List_of_all_titles)

    if Find_close_match:
        Close_match = Find_close_match[0]
        print(f"Closest Match: {Close_match}")
        Index_of_the_movie = movies_data[movies_data.title == Close_match]['index'].values[0]
    else:
        Find_close_match = difflib.get_close_matches(movie_name, List_of_all_genre)
        if Find_close_match:
            Close_match = Find_close_match[0]
            print(f"Closest Match: {Close_match}")
            Index_of_the_movie = movies_data[movies_data.genre == Close_match]['index'].values[0]
        else:
            Find_close_match = difflib.get_close_matches(movie_name, List_of_all_director)
            Close_match = Find_close_match[0]
            print(f"Closest Match: {Close_match}")
            Index_of_the_movie = movies_data[movies_data.director == Close_match]['index'].values[0]

    #Find the index of movie from the title
    Index_of_the_movie = movies_data[movies_data.title == Close_match]['index'].values[0]

    similarity_score = list(enumerate(similarity[Index_of_the_movie]))

    #Now we can sort this list according to similarity score from hgigh to low
    Sorted_similar_movies = sorted(similarity_score, key =lambda x:x[1],    reverse= True)

    #Print the name of similar movies based on the index
    print("Her's A list of Movies You Might Like...\n")

    i = 1
    lbox.pack(padx=10,pady=10,fill=BOTH, expand=True)
    lbox.insert(END, " ")
    # Button(root, text ="add", command=add).pack()
    for movies in Sorted_similar_movies:
        index = movies[0]
        tital_from_index = movies_data[movies_data.index == index]['title'].values[0]
        if (i <31):
            lbox.insert(ACTIVE, f"{int(i)}. {tital_from_index}")
            # lbox.insert(ACTIVE, f"{i}. {tital_from_index}")
            # print(f"{i}. {tital_from_index}")
            i+=1.
    

movies_data = pd.read_csv('movies.csv')
#feature selection
Selected_feature=['genres','keywords','tagline','cast','director']

#droping null values for only these columns
for feature in Selected_feature:
    movies_data[feature]= movies_data[feature].fillna("")

#Combining all 5 features in one 
Combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']

#Converting text to numeric value
Vectorizer = TfidfVectorizer()
feature_vector= Vectorizer.fit_transform(Combined_features)

#Find the similarity score by cosine similarity
similarity = cosine_similarity(feature_vector)



name = Label(root, text="Your Favourite Movie Name", bg="black", fg="white", padx=10, pady=10).pack(side="left" ,padx=5,pady=5)
# name.grid(row=1,column=2)
movie_name1 = StringVar()
movie_Entry = Entry(root, textvariable=movie_name1,font=("comicsansns",10,"bold" ), borderwidth=3,relief=SUNKEN).pack(side="left" ,padx=10,pady=10)


b1= Button(root, fg="red", text="Get Suggestions", bg="black",foreground='white', padx=5, pady=10, font=("comicsansns",10,"bold" ), borderwidth=3,relief=SUNKEN, command=getval).pack(side="left" ,padx=10,pady=10)
# b1.grid(row=1, column=4)




root.mainloop()
