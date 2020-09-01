import discord,datetime,requests,json,asyncio 

# Get OAuth token using client id & secret
def oauth(client_id,client_secret):
    token= requests.post(f"https://id.twitch.tv/oauth2/token"
    f"?client_id={client_id}"
    f"&client_secret={client_secret}"
    "&grant_type=client_credentials").json()['access_token']
    
    return token

def get_credentials():
    f = open(r'credentials.txt','r')
    credentials = f.readlines()
    return credentials

# GET request headers
def get_request(credentials):
    client_id = (credentials[0]).rstrip()
    client_secret = (credentials[1]).rstrip()
    params = None
    headers = {"Client-ID": client_id}
    token = oauth(client_id,client_secret)
    headers["Authorization"] = "Bearer {}".format(token)
    
    return client_id, client_secret, params, headers

# Send GET request, format into json
def get_results(channel,credentials):
    client_id, client_secret, params, headers = get_request(credentials)
    url = 'https://api.twitch.tv/helix/search/channels?query=%s' % (channel)
    r=requests.get(url, params=params, headers = headers)

    return (r.json())

# Check if channel is live 
def islive(channel,credentials):
    results = get_results(channel,credentials)
    return ((results['data'])[0])['is_live']

def timestamp():
    timestamp = "[" + str(datetime.datetime.now()) + "]"
    return timestamp

def tokenstamp():
    timestamp = int((datetime.datetime.now()).strftime("%H"))
    return timestamp
# -------------------------------------------------------------------------------

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(timestamp(),'Logged in as:',self.user.name, "id#:", self.user.id)
        print(" # -------------------------------")

    async def on_message(self, message):
        # Bot won't respond to its own messages
        if message.author == self.user:
            return
        print(timestamp(),"[",message.author,message.channel,"]",message.content)
        
    async def my_background_task(self):
        await self.wait_until_ready()
        # Loop
        while not self.is_closed():
            try:
                # Get account client id, secret, and discord chennel ID
                credentials = get_credentials()
                # Target twitch user's channel=
                user = input("Enter twitch name.")
                if islive(user,credentials):
                    print(timestamp(),'Channel is live!')
                    disc_channel = self.get_channel(int((credentials[2]).rstrip()))
                    await disc_channel.send("https://www.twitch.tv/%s" % (user))
                    await asyncio.sleep(18000)
                else:
                    await asyncio.sleep(60)
            except Exception as e:
                print(e)

client = MyClient()
client.run('')

