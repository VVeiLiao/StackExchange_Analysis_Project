#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Chianson Siu, Wei Liao
#
# Created:     13/02/2019
#-------------------------------------------------------------------------------
import pandas as pd
import operator

def removeBodyXMLTags(df):
    '''
    This function removes all XML tags in the "Body" column of the pandas data
    frame, e.g, all <p> and </p> tags should be removed.
    @param df is a pandas dataframe with one column that refers to the
              body of the text named "Body"
    @return a pandas datafame    
    '''

    # For each post in column "Body" of the panda dataframe
    # Remove all XML tags and put the result back to the
    # corresponding cell
    for i in range(len(df.index)):
        # Obtain cell content to edit
        postBody = df.at[i, "Body"]

        # Remove XML flasg and put result back to corresponding column
        df.at[i, "Body"] = removeXMLTags(str(postBody))
    return df


def removeXMLTags(text):
    '''
    Given a string of content, remove all occurences of XML tags.
    (XML tags is anything that starts with '<' and ends with '>')

    @param text String. A string of text.

    @return a String with all occurences of XML tags removed
    '''

    textList = list(text)
    # Remove All the XML tags
    j = 0
    while j < len(textList):
        if textList[j] == "<":
            while textList[j] != ">":
                textList.pop(j)
            textList.pop(j)
        else:
            j += 1

    # Convert list back into string and return the result
    return ''.join(textList)



def wordToCount(text):
    '''
    Given a string of content, count the number of occurence of each word,
    then returns the result.
    
    @param text String. A string of text.

    @return a dictionary mapping word to word count
    '''
    wordDict = dict()
    textList = text.split(" ")
    for word in textList:
        key = word.lower()
        wordDict[key] = wordDict.get(key, 0) + 1
    return wordDict


def top10Words(wordDict):
    '''
    Given a dictionary that maps word to its occurence count, return a
    list of top 10 highest occuring words

    @param wordDict Dictionary. A dictionary that maps a word to the 
                    number of times that it occured in a text

    @return a list of top 10 highest occuring words
    '''
    
    # Create list of words to exclude from final list
    exclude = ["the", "a", "of", "or", "an", "and", "because"]

    result = list()
    # Sort dictionary into tuples according to value
    # Creates a list of tuples (word, count) sorted from highest count
    # to lowest count
    sorted_words = sorted(wordDict.items(), key=operator.itemgetter(1),
        reverse=True)

    # Take only the top 10 word part of the sorted_words
    # Exclude the common non-meaning words such as "the",
    # "of", "or"
    for i in range(100):
        # Make sure i is not over the range of sorted_words
        # and result has 10 words
        if i >= len(sorted_words) or len(result) == 10:
            break

        # Append words that are not in the exclude list
        if sorted_words[i][0] not in exclude:
            result.append(sorted_words[i][0])
    return result


def q1():
    # Create q1 dataframe
    q1_df = pd.DataFrame(columns=('ID', 'Tags', 'Top10Keywords',
        'Length', 'AnswerCount'))

    # read in the CSV file to pandas dataframe. The CSV file must be coded as
    # UTF-8.
    posts_df = pd.read_csv("Posts.csv")
    posts_df = removeBodyXMLTags(posts_df)

    # Fill in PostID, Length, AnswerCount of each row
    for i in range(len(posts_df.index)):
        # obtain body of the post
        body = posts_df.at[i, "Body"]

        # Obain each column info
        ID = posts_df.at[i, "Id"]
        tags = posts_df.at[i, "Tags"]
        top10Keywords = top10Words(wordToCount(body))
        length = len(str(body))
        answerCount = posts_df.at[i, "AnswerCount"]

        # Add a new row in the q1 dataframe with the correct values
        q1_df.loc[i] = [ID, tags, top10Keywords, length, answerCount]

    print(q1_df)


def q2():
    q2_df = pd.DataFrame()


def q3():
    q3_df = pd.DataFrame()



def main():

    # Research Question 1 Analysis DONE!
    #q1()

    # Research Question 2 Analysis
    q2()

    # Research Question 3 Analysis

    # !!!!!!!!!!!!!!!! PROBLEM WITH COMMENTS.CSV !!!!!!!!!!!!!!!!!

    #df = pd.read_csv("Comments.csv")
    #print(df.loc[0, :])
    # tags_df = pd.read_csv("Tags.csv")
    #print(tags_df)

# If this file is run as a Python script (such as by typing
# "python tests.py" at the command shell), then run the following:
if __name__ == "__main__":
    main()

