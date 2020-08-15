import discord,random,re,os
import main
from ast import literal_eval

hello = ["Hello!", "Good to see you!", "Hi there.","Hey"]
yesno = ["Yes.","No.","...","Probably","YES!","Sure?",":+1:",
            ":-1:","Probably","Uncertain...","Oh Absolutely!","Never"]
thanks = ["You're welcome!","No Problem!","Anytime!","You're welcome!",
          "No Problem!","Anytime!","You're welcome!","No Problem!",
          "Anytime!","Well its only my job..."]
wut = ["Huh?","?","I don't really understand what you're asking.",
       "Could you please rephrase that?","Rephrase that please?",]


f = open('listIRL.txt','r+')
food_IRL = f.read()
f.close()
f = open('listONL.txt','r+')
food_ONL = f.read()
f.close()
# Choosing food list
food_IRL = literal_eval(food_IRL)
food_ONL = literal_eval(food_ONL)




# Initiate AI and training if necessary
chatbot = main.Chatty()
# Initiate Discord Bot Client
class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as', self.user)



    async def on_message(self, message):
        # Python-chan won't respond to its own messages
        if message.author == self.user:
            return
        food = 0


        
        # Takes message from user
        og_msg = message.content
        msg = og_msg.lower()
        print(msg)

        # await message.channel.send
        if '@!634753035796742206' in msg:
            # Initiate AI intents 
            answer = chatbot.chat(msg)
            print(answer)

            if 'test123' in msg:
                channel= client.get_channel(402970774220177412)#634940420371251230)
                await message.channel.send("File delivery")
                stonk = 'aapl'
                file = str('C:\\Users\\Kevan\\AppData\\Local\\Programs\\Python\\Python37-32\\AlgoTrading\\'+stonk.upper()+'.csv')
                await channel.send(file=discord.File(file))

            elif answer == 'greeting':
                await message.channel.send(random.choice(hello))
            elif answer == 'yesno':
                await message.channel.send(random.choice(yesno))
            elif answer == 'food':
                if 'irl' in msg:
                    print('food_IRL')
                    await message.channel.send(random.choice(food_IRL))
                elif 'online' in msg:
                    print('food_ONL')
                    await message.channel.send(random.choice(food_ONL))
                else:
                    food_FULL = food_ONL + food_IRL
                    print('food_FULL')
                    await message.channel.send(random.choice(food_FULL))
            elif answer == 'thanks':
                await message.channel.send(random.choice(thanks))
            elif answer == 'add':
                try:
                    f_choice = ''.join(re.findall(r'[\"]{1}[\S]+[\s]*[\S]*[\s]*[\S]*[\s]*[\S]*[\s]*[\S]*[\s]*[\S]*[\"]{1}', msg))[1:-1]
                    if len(f_choice) == 0:
                        raise Error
                    if 'irl' in msg:
                        try:
                            food = food + 1
                            f = open('listIRL.txt','w+')
                            food_IRL.append(f_choice)
                            f.write(food_IRL)
                            f.close()
                            await message.channel.send("Adding to IRL list")
                        except:
                            food = 0
                            await message.channel.send("Specify with a food choice! (e.g. Add \"McDonald's\" to the IRL list.)")
                    if 'online' in msg or 'delvery' in msg:
                        try:
                            food = food + 10
                            f = open('listONL.txt','w+')
                            food_ONL.append(f_choice)
                            f.write(food_ONL)
                            f.close()
                            await message.channel.send("Adding to Online list")
                        except:
                            food = 0
                            await message.channel.send("Specify with a food choice! (e.g. Add \"McDonald's\" to the online list.)")
                    else:
                        food = 111
                        await message.channel.send("Specify a list please! [IRL or Online]")
                except:
                    await message.channel.send("No food choice was found... (Try using a format like this: Add \"McDonal's\" to IRL list.)")
                        
            elif food == 111 and 'irl' in msg or 'online' in msg:
                if 'irl' in msg:
                    f = open('listIRL.txt','w+')
                    food_IRL.append(f_choice)
                    f.write(food_IRL)
                    f.close()
                elif 'online' in msg:
                    f = open('listONL.txt','w+')
                    food_ONL.append(f_choice)
                    f.write(food_ONL)
                    f.close()
                    
            else:
                await message.channel.send(random.choice(wut))

                
# Initiate Discord client
client = MyClient()
client.run('') #Insert Discord token
