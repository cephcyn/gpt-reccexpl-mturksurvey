# Survey Distribution Notes

## Dataset

To show a set of mildly customizable movie suggestions and texts for each participant, we needed to collect a broad set of relatively well-known movies to base suggestions on (the "seed" movie), a set of suggestions for each seed movie, and a set of human-generated and model-generated texts for each suggested movie.

To collect seed and suggestion movies, we used the [MovieLens dataset](https://movielens.org)(2023/04/26), together with [IMDB](https://www.imdb.com/)(2023/04/26) and [BestSimilar](https://bestsimilar.com/)(2023/04/26).

We manually selected 10 well-known seed movies to ideally cover a range of movie genres, as well as raise the chance of most participants recognizing at least one seed movie.
We applied these requirements for seed movies:
- Must be a work of fiction
- Must have a modern U.S. MPA rating below R (only G, PG, PG-13 were allowed)
- Must have at least 45,000 MovieLens reviews

For each seed movie, we collected a sorted list of similar movies using the first 5 pages of "similar movies" on MovieLens followed by 1 page of "similar movies" on BestSimilar.
We selected the top 5 movies on this last after applying these requirements:
- Must be a work of fiction
- Must have a modern U.S. MPA rating below R (only G, PG, PG-13 were allowed)
- May _not_ be a TV-only, international-only, or documentary film
- Must be released before 2023 (to avoid films that were showing in theaters)
- Must have duration at least 30 minutes long (to avoid demo animations and short films)
- Must have at least 5 stars on IMDB
- Must have at most 80,000 IMDB score ratings
- May _not_ be overlapping in franchise (e.g. if one Winnie the Pooh movie is already included, any following Pooh-branded movies are excluded)

For each movie suggestion, we collected 5 human-generated reviews to use as a baseline comparison.
These reviews consisted of the top 5 most "featured" non-spoiler reviews on IMDB (as of 2023/04/26, "featured" reviews seem to use a metric combining high helpfulness vote percentage and high total vote counts) for each movie.
IMDB movie review format includes both a review title and review text, but multiple reviewers referenced their titles in the review texts.
To handle this, we prepended review title to the review text.

For each movie suggestion, we also synthesized one model-generated text using the 5 human-generated reviews as a source of information about the movie.
We used ["gpt-3.5-turbo-0301" from OpenAI](https://platform.openai.com/docs/api-reference/chat) with a custom system prompt instructing GPT that it is a movie recommender bot, a custom chat prompt instructing GPT to write a short review in the style of a friendly recommendation with the 5 human-generated reviews provided as reference material, and default hyperparameters.

The exact prompt structure (using R1, R2, etc. as variables containing the raw human review titles+texts):
```
messages=[
  {
    'role':'system', 
    'content':'You are a friendly movie recommender bot that gives people the most accurate information you can.'
  },
  {
    'role':'user', 
    'content':f'Please write a 75 to 100 word review of this movie, in the style of a friendly recommendation. Keep in mind that you have not watched this movie yourself.\nHere are some other reviews aboout this movie to help you out:\n1. {R1}\n2. {R2}\n3. {R3}\n4. {R4}\n5. {R5}'
  },
]
```
Sometimes the first user message exceeded max input length, so we truncated the user-content text (the prompt) to maximum length 4097 when appropriate.

Finally, we took the human-generated and model-generated texts, reformatted them to remove all linebreaks and extraneous whitespace, and truncated them to 100 tokens when necessary (with "..." append in these cases to indicate that further text was not shown).
In summary, there are 10 well-known seed movies, 5 lesser-known suggestions based on each seed movie (50 total), 5 human-generated reviews for each suggestion (250 total), and 1 model-generated review for each suggestion (50 total).

The exact movies and associated review texts used are available in this repository:
- [moviereviewcollection_human.csv](moviereviewcollection_human.csv)
- [moviereviewcollection_model.csv](moviereviewcollection_model.csv)

These reviews were imported into Qualtrics via manual copy-paste.
(Please let us know how to improve Qualtrics survey implementation if you have tips.)

## Survey Procedure

We generated condition codes to ensure balanced representation between human-generated and bot-generated texts for each movie, as well as between different human authors of the human-generated texts.
Each participant was assigned one condition code that determines which of the 6 review texts is shown for each individual movie suggestion, as well as if they are shown sources for all review texts.
Condition codes were balanced such that:
- For each movie, there are an equal number of model-generated vs human-generated texts shown in total.
- For the human-generated texts for each movie, there are an equal number of times each human review is represented.
- For each text, the number of times it is shown with authorship credit or not is balanced.

Survey participants went through the following steps in order.
1. They were initially shown the consent form with information about the payment scheme and a brief introduction to the purpose and contents of the survey.
2. They were asked to select one of the seed movies to base movie suggestions on.
3. Participants were shown the 5 relevant movie suggestions for their chosen seed movie, together with review texts for each suggestion.
    - Authorship and review texts shown were based on the participant's condition code.
    - The 5 movie suggestions were shown in random order to reduce order bias.
    - Participants were asked to rank these movies from 1 to 5 in order of how interested they were in watching (or rewatching) each movie.
    - On the same page, participants were also asked to indicate which suggestions they had seen before.
4. For each suggested movie (in random order), participants were asked to give ratings for how accurate (only if they had seen the movie before), informative, persuasive, and interesting the texts were, as well as elaborate on what aspects of the text satisfied or did not satisfy these attributes.
    - They were also asked if they would be interested in reading more reviews from the same author in the future.

