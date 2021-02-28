from collections import defaultdict
import re
import gensim
from gensim.utils import tokenize
from fuzzywuzzy import process
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
# nltk.download('brown')
from nltk.corpus import brown

def normalize_time(timestamps):

    # Normalize timestamp to "hh mm ss"

    normalized_time = []

    for timestamp in timestamps:
        seconds = int(timestamp)
        minutes = seconds//60
        hours = minutes//60
        minutes = minutes%60
        seconds = seconds%60

        normalized_timestamp = ''

        if hours != 0:
            normalized_timestamp += str(hours) + 'h '
        normalized_timestamp += str(minutes)+'m '+str(seconds)+'s'

        normalized_time.append(normalized_timestamp)

    return normalized_time

def pretty_print(output):
    """
    Method to output the relevant captions and timestamps in a pretty manner.

    @param output: A list of pairs where each pair = (caption, timestamp)

    """
    spaces = max([len(caption) for caption, timestamp in output])
    spaces += 5
    for caption, timestamp in output:
        print(caption, end=' '*(spaces - len(caption)))
        print(timestamp)

def parse_youtube_url(video_url):

    youtube = r'(youtu.be\/|v\/|e\/|u\/\w+\/|embed\/|v=)'
    video_id = r'([^#\&\?]*).*'
    https = r'^.*'

    parsed_url = re.search(https + youtube + video_id, video_url)

    return parsed_url[2]


def get_youtube_transcript(video_url, languages=None):

    if languages is None:
        languages = ['en']

    video_id = parse_youtube_url(video_url)
    data = dict()

    try:
        data = YouTubeTranscriptApi.get_transcript(video_id, languages)
    except Exception as e:
        print(e, type(e))
    
    transcript = defaultdict(float)

    for vid_data in data:
        transcript[vid_data['text'].lower()] = vid_data['start']

    return transcript

def setup():

    sentences = brown.sents()
    model = gensim.models.Word2Vec(sentences, min_count=1)

    vocabulary = defaultdict(int)

    for sentence in sentences:
        for word in sentence:
            vocabulary[word] = 1
    
    return model, vocabulary


class Searcher:
    def __init__(self):
        self._fuzzy_ = "FUZZY"
        self._semantic_ = "SEMANTIC"

        self.model, self.vocabulary = setup()

    def get_captions_by_fuzzy_similality(self, query, corpus, limit=5):

        similar_strings = process.extractBests(query, corpus, limit=limit)
        required_strings = [caption for caption, similarity in similar_strings]

        return required_strings
    
    def get_captions_by_semantic_similality(self, query, corpus, limit=5):

        captions_and_similarities = []
        corpus = list(corpus)

        for idx, caption in enumerate(corpus):
            similarity = self.compute_semantic_similarity(query, caption)
            captions_and_similarities.append([similarity, idx])

        captions_and_similarities.sort()
        captions_and_similarities = captions_and_similarities[:limit]

        closest_captions = []

        for similarity, idx in captions_and_similarities:
            closest_captions.append(corpus[idx])
        
        return closest_captions

    def compute_semantic_similarity(self, sentence_1, sentence_2):

        sentence_1 = list(tokenize(sentence_1))
        sentence_2 = list(tokenize(sentence_2))

        visited_1 = [0]*len(sentence_1)
        visited_2 = [0]*len(sentence_2)

        similarity = 0

        # for each word in sentence_1, we find the closest un-mapped word in sentence_2 and add this similarity.

        for idx_a, word_a in enumerate(sentence_1):
            if self.vocabulary[word_a] == 1:
                visited_1[idx_a] = 1
                closest_distance = 1e18
                idx_chosen = -1
                for idx_b, word_b in enumerate(sentence_2):
                    if visited_2[idx_b] == 0 and self.vocabulary[word_b] == 1:
                        current_distance = (1 - self.model.similarity(word_a, word_b))
                        if idx_chosen == -1 or current_distance < closest_distance:
                            closest_distance = min(closest_distance, current_distance)
                            idx_chosen = idx_b

                if idx_chosen != -1:
                    visited_2[idx_chosen] = 1

                similarity += closest_distance

        return similarity/len(sentence_1)

    

    def get_timestamp(self, query, caption_to_timestamp, mode="FUZZY", limit=5):

        if mode == self._fuzzy_:
            highest_similarity_captions = self.get_captions_by_fuzzy_similality\
                (query, caption_to_timestamp.keys(), limit=limit)

        if mode == self._semantic_:
            highest_similarity_captions = self.get_captions_by_semantic_similality\
                (query, caption_to_timestamp.keys(), limit=limit)
            
        marked_timestamps = [caption_to_timestamp[caption] for caption in highest_similarity_captions]
        
        return marked_timestamps
            

    def main(self, video_url, query, limit=5, languages=None, mode="FUZZY"):
        print('url', video_url)
        print('query:', query)

        query = query.lower()
        data = get_youtube_transcript(video_url, languages)

        print('Transcript downloaded')
        timestamps = self.get_timestamp(query, data, limit=limit, mode=mode)

        timestamps_captions = defaultdict(str)

        for caption in data:
            key = data[caption]
            value = caption
            timestamps_captions[key] = value
        
        captions_extracted = []
        for timestamp in timestamps:
            captions_extracted.append(timestamps_captions[timestamp])

        pretty_print(list(zip(captions_extracted, normalize_time(timestamps))))
        # pretty_print(list(zip(captions_extracted, timestamps)))
        # return list(zip(captions_extracted, normalize_time(timestamps_captions)))
        return list(zip(captions_extracted, timestamps_captions))


# search_engine = Searcher()

# def get_search_engine():
#     return search_engine

if __name__ == "__main__":

    # url = "https://www.youtube.com/watch?v=bfHEnw6Rm-4"
    # url = "https://www.youtube.com/watch?v=bfHEnw6Rm-4"
    url = "https://www.youtube.com/watch?v=4JWG6hmAJpg"
    query = "idiot"
    limit = 10
    languages = ['en']
    mode = 'FUZZY'

    Search = Searcher()
    Search.main(url, query=query, limit=limit, languages=languages, mode=mode)