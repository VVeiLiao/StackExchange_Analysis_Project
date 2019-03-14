#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Chianson Siu, Wei Liao
#
# Created:     13/02/2019
#-------------------------------------------------------------------------------
import nltk
from nltk.corpus import stopwords
from collections import Counter
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
    textList = str(text).split(" ")
    for word in textList:
        key = word.lower()
        if key != " " and key != "":
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
    exclude = set(stopwords.words('english'))

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


def filter10User(users_df):
    '''
    Takes a user data frame. Filters out the first 10 users and store the
    results in a dictionary with key being the user ID and the value being
    the user's reputation score

    @param users_df Pandas datagrame. The datafram that contains information
                    on users.

    @return a dictionary of the first 10 users (key is user ID, value is
            reputation)
    ''' 
    result = dict()
    for i in range(10):
        # Make user dataframe has at least 10 entries
        if len(users_df.index) > 10:
            # Take the first 10 Id and Reputation out
            section = users_df.head(n=10)[["_Id", "_Reputation"]]
            # Store ID as key and Reputation as value
            result[section.iloc[i, 0]] = section.iloc[i, 1]
    return result


def numWords(text):
    '''
    Count the number of words there is in a block of string
    '''
    textList = text.split(" ")
    return len(textList)


def tagCount(text):
    textList = list(str(text))
    # take the words between the "<>"
    wordString = ""
    j = 0
    while j < len(textList):
        if textList[j] == "<":
            # pop out the first "<"
            textList.pop(j)
            while textList[j] != ">":
                wordString += textList.pop(j)
            textList.pop(j)
            wordString += " "
        else:
            j += 1

    tag_dict = wordToCount(wordString)
    return tag_dict

def q1(posts_df):
    '''
    Performs tasks necessary to solve research question 1
    '''

    # Create variables
    ans_tag = dict()
    ans_body = dict()
    ans_title = dict()
    ans_len = 0
    ans_count = 0
    
    noAns_tag = dict()
    noAns_body = dict()
    noAns_title = dict()
    noAns_len = 0
    noAns_count = 0

    # Fill in PostID, Length, AnswerCount of each row
    for i in range(len(posts_df.index)):
        body = posts_df.at[i, "Body"]

        # Obain each column info
        tags = tagCount(posts_df.at[i, "Tags"])
        top10Body = wordToCount(body)
        length = numWords(str(body))
        title = wordToCount(posts_df.at[i, "Title"])

        # Add a new row in the ans or no_ans dataframe with the correct values
        if pd.isnull(posts_df.loc[i, "AcceptedAnswerId"]):
            # There is no accepted answer
            noAns_tag = Counter(noAns_tag) + Counter(tags)
            noAns_body = Counter(noAns_body) + Counter(top10Body)
            noAns_title = Counter(noAns_title) + Counter(title)
            noAns_len += length
            noAns_count += 1
        else:
            ans_tag = Counter(ans_tag) + Counter(tags)
            ans_body = Counter(ans_body) + Counter(top10Body)
            ans_title = Counter(ans_title) + Counter(title)
            ans_len += length
            ans_count += 1

    
    print("noAns_tag:", top10Words(noAns_tag))
    print("noAns_body:", top10Words(noAns_body))
    print("noAns_title:", top10Words(noAns_title))
    print("noAns Average Length:", float(noAns_len/noAns_count))

    print()

    print("ans_tag:", top10Words(ans_tag))
    print("ans_body:", top10Words(ans_body))
    print("ans_title:", top10Words(ans_title))
    print("ans Average Length:", float(ans_len/ans_count))


def q2(posts_df, users_df):
    '''
    Performs tasks necessary to solve research question 2
    '''
    q2_df = pd.DataFrame(columns=("UserID", "Reputation", "AnswerCount", 
        "AverageBodyLength"))

    # Get UserID and Reputation first
    q2_df.loc[ : , "UserID"] = users_df.loc[ : , "_Id"]
    q2_df.loc[ : , "Reputation"] = users_df.loc[ : , "_Reputation"]

    # id to length and count dictionary
    id_lenCount = dict()

    # Find which posts are answers
    ans_set = set()
    for i in range(len(posts_df.index)):
        # this post is an answer
        if int(posts_df.at[i, "PostTypeId"]) == 2:
            ans_set.add(posts_df.at[i, "Id"])

    # Fill in answer count and accumulate body length for now
    for i in range(len(posts_df.index)):
        userID = posts_df.at[i, "OwnerUserId"]
        # add only if userID exist and if the post is an answer
        if userID in q2_df.loc[ : , "UserID"] and posts_df.at[i, "Id"] in ans_set:
            if userID not in id_lenCount.keys():
                # list first element is count, second is accumulated body len
                id_lenCount[userID] = list()
                id_lenCount[userID].append(0)
                id_lenCount[userID].append(numWords(str(posts_df.at[i, "Body"])))
            else:
                id_lenCount[userID][0] += 1
                id_lenCount[userID][1] += numWords(str(posts_df.at[i, "Body"]))

    # Now fill average length and answer count back into the main table
    for i in range(len(q2_df.index)):
        userID = q2_df.at[i, "UserID"]
        if userID in id_lenCount.keys():
            answerCount = id_lenCount[userID][0]
            q2_df.at[i, "AnswerCount"] = answerCount
            if answerCount != 0:
                q2_df.at[i, "AverageBodyLength"] = id_lenCount[userID][1]/answerCount

    q2_df = q2_df.dropna()

    q2_df.to_excel("Q2_Result.xlsx")


def q3(users_df):
    '''
    Performs tasks necessary to solve research question 3
    '''
    q3_df = pd.DataFrame(columns=("UserID", "Reputation", "UpVotes",
        "DownVotes"))

    # extract the userID, reputation, upvotes, and downvotes
    q3_df.loc[ : , "UserID"] = users_df.loc[ : , "_Id"]
    q3_df.loc[ : , "Reputation"] = users_df.loc[ : , "_Reputation"]
    q3_df.loc[ : , "UpVotes"] = users_df.loc[ : , "_UpVotes"]
    q3_df.loc[ : , "DownVotes"] = users_df.loc[ : , "_DownVotes"]

    # remove rows with any zeros
    q3_df = q3_df[(q3_df != 0).all(1)]

    #print(q3_df)
    q3_df.to_excel("Q3_Result.xlsx")

def main():
    # read in the CSV file to pandas dataframe. The CSV file must be coded as
    # UTF-8.
    posts_df = pd.read_csv("Posts2018.csv")
    posts_df = removeBodyXMLTags(posts_df)

    # Research Question 1 Analysis DONE! (fix stopword list)
    q1(posts_df)

    users_df = pd.read_csv("Users.csv")

    # Research Question 2 Analysis DONE! (accepted answer post only?)
    #q2(posts_df, users_df)

    # Research Question 3 Analysis
    #q3(users_df)

  #  df = pd.read_csv("Comments.csv")
   # print(df.loc[0, :])


# If this file is run as a Python script (such as by typing
# "python tests.py" at the command shell), then run the following:
if __name__ == "__main__":
    main()