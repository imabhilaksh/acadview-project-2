
import requests,urllib
from token import token,token1

base_url='https://api.instagram.com/v1/'

def get_user_post(insta_username):
    user_id=get_user_id()



def get_own_post():
    requesturl=(base_url+'users/self/media/recent/?access_token=%s')%(token1)
    user_info=requests.get(requesturl).json()

    if user_info['meta']['code']==200 or user_info['meta']['code']==304:
        if len(user_info['data']):
            image_name=user_info['data'][0]['id']+'.jpeg'
            image_url=user_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "image downloaded"
        else:
            print "No such post"
    else:
        'Other code returned '



def get_user_id(insta_username):
    request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, token)

    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
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
    request_url = (base_url + 'users/%s?access_token=%s') % (user_id, token)
    print 'GET request url : %s' % (request_url)
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
    request_url = (base_url + 'users/self/?access_token=%s') % (token1)
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
    print "Enter your choice "
    print '1. Own Information '
    print '2. Get own recent post'
    while start:
        choice = int(raw_input())
        if(choice==1):
            self_info()
        elif choice==2:
            get_own_post()
        else:
            print 'Exit '
            start=False

start_bot()
