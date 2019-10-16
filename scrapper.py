# Get misc. Q&As from https://www.triviaquestionss

import sys, os, requests, bs4


def scrapper(url, topic):

    # Create the folder and text file
    name_q = 'questions_{0}.txt'.format(topic)
    name_ans = 'answers_{0}.txt'.format(topic)
    os.makedirs('{0}_questions_dir'.format(topic), exist_ok=True)
    os.makedirs('{0}_answers_dir'.format(topic), exist_ok=True)
    q_file = os.path.join('{0}_questions_dir'.format(topic), name_q)
    ans_file = os.path.join('{0}_answers_dir'.format(topic), name_ans)

    # Get the html page
    link = requests.get(url)
    bs = bs4.BeautifulSoup(link.text, 'html.parser')

    q_list = bs.select('h3')
    ans_list = bs.select('p')

    # Open a reference to the file to write to
    q_file_ref = open(q_file, 'w')
    ans_file_ref = open(ans_file, 'w')

    # Write to the file as you loop through the element
    for elem in q_list:
        q_file_ref.write(elem.getText() + '\n')

    for elem in ans_list:
        ans_file_ref.write(elem.getText() + '\n')

    q_file_ref.close()


if __name__ == '__main__':
    scrapper("https://www.triviaquestionss.com/animal-trivia-questions/", "wildlife")
    scrapper("https://www.triviaquestionss.com/history-trivia-questions/", "history")
    scrapper("https://www.triviaquestionss.com/science-trivia-questions-kids/", "science_for_kids")
    scrapper("https://www.triviaquestionss.com/trivia-questions-for-kids/", "misc_trivia_for_kids")
    scrapper("https://www.triviaquestionss.com/geography-trivia-questions/", "geography")
    scrapper("https://www.triviaquestionss.com/science-trivia-questions-with-answers/", "science")
    scrapper("https://www.triviaquestionss.com/food-trivia-questions/", "food")
    scrapper("https://www.triviaquestionss.com/tv-trivia-questions/", "tv")
    scrapper("https://www.triviaquestionss.com/thanksgiving-trivia-questions/", "thanksgiving")
    scrapper("https://www.triviaquestionss.com/80s-trivia-question-and-answer/", "music_80s")
    scrapper("https://www.triviaquestionss.com/90s-music-trivia-questions/", "music_90s")
