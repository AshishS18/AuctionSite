import requests


def get_users(id):
    print(id)
    if id is None:
        url = 'http://127.0.0.1:8000/userlist'
    else:
        url = 'http://127.0.0.1:8000/userlist'+'/'+str(id)
    r = requests.get(url)
    users = r.json()
    users_list = {'users': users}
    return users_list


def get_auctions(id):
    if id is None:
        url = 'http://127.0.0.1:8000/auctionlist'
    else:
        url = 'http://127.0.0.1:8000/auctionlist'+'/'+str(id)
    r = requests.get(url)
    auctions = r.json()
    auctions_list = {'auctions': auctions}
    return auctions_list


def get_bids(id):
    if id is None:
        url = 'http://127.0.0.1:8000/bidlist'
    else:
        url = 'http://127.0.0.1:8000/bidlist'+'/'+str(id)
    r = requests.get(url)
    bids = r.json()
    bids_list = {'bids': bids}
    return bids_list
