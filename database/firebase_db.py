from firebase import firebase
import convert_format_date

url = 'https://cos4105-da928.firebaseio.com/'
action = firebase.FirebaseApplication(url, None)

def create_data(scrapped, name_news, topic):
    if topic == "economic":
        topic = topic + "s"
    for i in range(len(scrapped)):
        postfix_url = scrapped[i][0][-7:]
        action.put('/'+name_news+'/'+topic, postfix_url, scrapped[i])

def read_data(name_news, topic):
    result = action.get('/'+name_news, topic)
    return result

def detele_data(name_news, topic):
    action.delete('/'+name_news, topic)

#-----------------------------------------------------

if __name__ == '__main__':
    pass
