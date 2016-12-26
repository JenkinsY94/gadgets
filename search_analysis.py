# -*- coding: utf-8 -*-

from os import path
import io, operator, json
import matplotlib
import matplotlib.pyplot as plt 
from wordcloud import WordCloud,STOPWORDS
import jieba
import datetime

def rank_query(filename):
    query = {}
    stopw = set([line.strip().decode('utf-8') for line in open('stopwords.txt').readlines()])
    for file in filename:
        with io.open(file,'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['event']:
                raw = i['query']['query_text']
                separated_query = raw.split(' ')
                for word in separated_query:
                    seg_query = jieba.cut(word, cut_all=False)
                    for s in seg_query:
                        if s not in stopw:
                            if not query.get(s):
                                query[s] = 1
                            else:
                                query[s] += 1   
    # sorting query by value, return list of tuples. 
    # remain those search times>15
    sorted_query = sorted(query.items(), key=operator.itemgetter(1))[::-1]
    total_cnt = sum([i[1] for i in sorted_query])
    print "total cnt is: %d" % total_cnt
    sorted_query = [i for i in sorted_query if i[1]>15]
    major_cnt = sum([i[1] for i in sorted_query])
    print "major cnt is: %d" % major_cnt
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(range(len(sorted_query)),[i[1] for i in sorted_query],align='center')
    plt.xticks(range(len(sorted_query)),[i[0] for i in sorted_query], rotation='vertical')
    plt.margins(0.1)
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def all_query(filename):
    query = []
    stopw = set([line.strip().decode('utf-8') for line in open('stopwords.txt').readlines()])
    for file in filename:
        with io.open(file,'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['event']:
                raw = i['query']['query_text']
                separated_query = raw.split(' ')
                for word in separated_query:
                    seg_query = jieba.cut(word, cut_all=False)
                    # stopwords elimination
                    for s in seg_query:
                        if s not in stopw:
                            query.append(s)
    query_str = u' '.join(query)
    return query_str

# visualization
def word_cloud_visual(words):
        wordcloud = WordCloud(font_path='C:/Windows/Fonts/simkai.ttf',
                              # stopwords=STOPWORDS,
                              background_color='black',
                              width=1200,
                              height=1000
                             )
        wordcloud = wordcloud.generate(words)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

# plot each month's search times for the specified words 
def plt_word_trends(filename, wordlist):
    line = ['None' for i in range(len(wordlist))]
    plt.xkcd()
    for i in range(len(wordlist)):
        timestamps = []
        months = [m for m in range(1,13)]
        month_kv = {key: 0 for key in months}
        for file in filename:
            with io.open(file,'r', encoding='utf-8') as f:
                data = json.load(f)
                for d in data['event']:
                    raw = d['query']['query_text']
                    separated_query = raw.split(' ')
                    for w in separated_query:
                        if w == wordlist[i]:
                            t = float(d['query']['id'][0]['timestamp_usec'])/10**6
                            timestamps.append(t)
        for t in timestamps:
            m = datetime.datetime.fromtimestamp(t).month
            if not month_kv.get(m):
                month_kv[m] = 1
            else:
                month_kv[m] += 1
        sorted_month = sorted(month_kv.items(), key=operator.itemgetter(0))
        # plot
        line[i],= plt.plot(months,[m[1] for m in sorted_month],label=wordlist[i])
    plt.legend(handles=line, loc=2)
    plt.xlabel('month')
    plt.ylabel('search times')
    plt.show()
    

# plot search times of each month
def plt_search_times(filename):
    timestamps = []
    months = [m for m in range(1,13)]
    month_kv = {key: 0 for key in months}
    for file in filename:
        with io.open(file,'r', encoding='utf-8') as f:
            data = json.load(f)
            for d in data['event']:
                t = float(d['query']['id'][0]['timestamp_usec'])/10**6
                m = datetime.datetime.fromtimestamp(t).month
                month_kv[m] += 1
    print month_kv
    plt.xkcd()
    plt.bar(range(len(month_kv)),month_kv.values(),align='center')
    plt.xticks(range(len(month_kv)),month_kv.keys())
    plt.show()


def main():
    filename = ['2016-01-01.json',
                '2016-04-01.json',
                '2016-07-01.json',
                '2016-10-01.json']
    # plot word cloud of all queries
    words = all_query(filename)
    word_cloud_visual(words)

    # plot trending of specified wordlist, each word in one line
    plt_word_trends(filename, ['java','python','matlab','minizinc'])
    
    # plot seatch times in each month
    plt_search_times(filename)
    
    # plot each query's search time, in descending order
    rank_query(filename)

if __name__ == '__main__':
    main()