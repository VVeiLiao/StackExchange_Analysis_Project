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
	count = 0
	for word in text:
		count += 1
	return count

def make(post_df):

	res_df = DataFrame(columns=('UserID', 'AnsCount', 'AnsAverageLen', 'Reputation'))

	for i in range(len(post_df.index)):
		if posts_df.at[i, "OwnerId"] in posts_df[ : , "AcceptedAnswerId"]:

			res_df

	# iterate through post, 
	# if postID is in acceptedAnswerID list,
	#    put OwnerUserID, Body word count in result table
	#    update number of answer in result table
	# if post is this aaID then get OwnerUserID and Body (count)


def q1():
    '''
    Performs tasks necessary to solve research question 1
    '''

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

    # print(q1_df)


def q2(users_df):
    '''
    Performs tasks necessary to solve research question 2
    '''
    q2_df = pd.DataFrame(columns=("UserID", "Reputation", "AnswerLength",
        "PostLength", "CommentLength", "AnswerKeyWord", "PostKeyWord",
        "CommentKeyword", "QuestionKeyword"))

    # Sort user by highest reputation
    sorted_df = users_df.sort_values("_Reputation", ascending=False)
    user_rep_dict = filter10User(sorted_df)


def q3(users_df):
    '''
    Performs tasks necessary to solve research question 3
    '''
    q3_df = pd.DataFrame(columns=("UserID", "Reputation", "AnswerLength",
        "PostLength", "CommentLength", "AnswerKeyWord", "PostKeyWord",
        "CommentKeyword", "QuestionKeyword"))

    # Sort user by lowest reputation
    sorted_df = users_df.sort_values("_Reputation")
    user_rep_dict = filter10User(sorted_df)



def main():

    # Research Question 1 Analysis DONE!
    #q1()

    users_df = pd.read_csv("Users.csv")

    # Research Question 2 Analysis
    #q2(users_df)

    # Research Question 3 Analysis
    #q3(users_df)

    # !!!!!!!!!!!!!!!! PROBLEM WITH COMMENTS.CSV !!!!!!!!!!!!!!!!!

  #  df = pd.read_csv("Comments.csv")
   # print(df.loc[0, :])
    # tags_df = pd.read_csv("Tags.csv")
    #print(tags_df)


    # test num_words()

# If this file is run as a Python script (such as by typing
# "python tests.py" at the command shell), then run the following:
if __name__ == "__main__":
    main()

