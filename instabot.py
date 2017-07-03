import requests,urllib
import matplotlib.pyplot as plt
from app_access_token import ab
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#friends : imabhilaksh,aabshaar542

list=[]
list1=[]
base_url='https://api.instagram.com/v1/'



def plotting(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, ab)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    list1.append(comment_text)
                    print 'Negative comment : %s' % (comment_text)

                else:
                    list.append(comment_text)
                    print 'Positive comment : %s\n' % (comment_text)
            labels = 'positive', 'negative'
            sizes = [len(list), len(list1)]
            colors = ['gold', 'yellowgreen']
            explode = (0.05, 0)  # explode 1st slice

            # Plot
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=140)

            plt.axis('equal')
            plt.show()


        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def recent_media_liked():
    request_url=(base_url+'users/self/media/liked?access_token=%s')%(ab)
    id=requests.get(request_url).json()
    if id['meta']['code']==200 or id['meta']['code']==304:
        if len(id['data']):
            image_name = id['data'][0]['id'] + '.jpeg'
            image_url = id['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "Image downloaded"
        else:
            print "No such post"
    else:
        'Other code returned '


def get_comment_list(insta_username):
    id=get_post_id(insta_username)
    request_url=(base_url+'media/%s/comments?access_token=%s')%(id,ab)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            item=0
            number=1
            for element in user_info['data']:
                print ('%d. %s')%(number,element['text'])
                item+=1
                number+=1
            print "Successfully printed the list of comments "
        else:
            print "no comments "
    else:
        print "other error code returned "



def comment(insta_username):
    id=get_post_id(insta_username)
    text = raw_input("Enter your comment : ")
    payload = {"access_token": ab, "text": text}
    request_url = (base_url + 'media/%s/comments') % (id)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200 or make_comment['meta']['code']==304:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"




def get_post_id(insta_username):
    id=get_user_id(insta_username)
    if id==None:
        print "User does not exist "
        exit()
    request_url=(base_url+'users/%s/media/recent/?access_token=%s')%(id,ab)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            print 'No post '
    else:
        print "Other error code returned  "




def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url + 'media/%s/likes') % (media_id)
    payload = {"access_token": ab}
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful.'




def get_user_post(insta_username):
    id=get_user_id(insta_username)
    if id==None:
        print "No such user"
        exit()
    request_url=(base_url+'users/%s/media/recent/?access_token=%s')%(id,ab)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            image_name = user_info['data'][0]['id'] + '.jpeg'
            image_url = user_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "image downloaded "
        else:
            print "post does not exist "
    else:
        print "other error code returned "





def get_own_post():
    requesturl=(base_url+'users/self/media/recent/?access_token=%s')%(ab)
    user_info=requests.get(requesturl).json()

    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            image_name=user_info['data'][0]['id']+'.jpeg'
            image_url=user_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "Image downloaded"
        else:
            print "No such post"
    else:
        'Other code returned '





def get_user_id(insta_username):
    request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, ab)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()





def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User  not exist!'
        exit()
    request_url = (base_url + 'users/%s?access_token=%s') % (user_id,ab)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'





def self_info():
    request_url = (base_url + 'users/self/?access_token=%s') % (ab)
    user_info = requests.get(request_url)
    user_info=user_info.json()
    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User not found!'
    else:
        print 'exit'





def start_bot():
    start=True
    print "WELCOME TO INSTAGRAM BOT "
    while start:
        print '\n1. Get Self Information '
        print "2. Get other User's Information"
        print "3. Get own recent post "
        print "4. Get other user's post  "
        print "5. Like other user's post  "
        print "6. Comment on other post  "
        print "7. Get list of comments on other post "
        print "8. Get recent media liked by self "
        print "9. Positive vs Negative Comments  "
        print "10.Exit"
        print "Enter your choice \n"
        choice = int(raw_input())
        if(choice==1):
            self_info()
        elif choice==2:
            username=raw_input("Enter username : ")
            get_user_info(username)
        elif choice==3:
            get_own_post()
        elif choice==4:
            username = raw_input("Enter username : ")
            get_user_post(username)
        elif choice==5:
            username=raw_input("Enter username : ")
            like_a_post(username)
        elif choice==6:
            username=raw_input("Enter username : ")
            comment(username)
        elif choice==7:
            username=raw_input("Enter the username : ")
            get_comment_list(username)
        elif choice==8:
            recent_media_liked()
        elif choice==9:
            username=raw_input("Enter the username : ")
            plotting(username)
        elif choice==10:
            print 'Exit '
            start=False
        else:
            print "Invalid choice "



start_bot()