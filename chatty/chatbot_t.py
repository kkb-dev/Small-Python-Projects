import warnings, os 
# Ignore FutureWarnings from other modules used in main.py 
warnings.simplefilter(action='ignore', category=FutureWarning)
# Ignore warning indicating use of AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Import AI module
import main



# Call AI class object
x = main.Chatty()

# Create interface to talk with chatbot
while True:
    print('\n------------------------------')
    inp = input("[Type 'quit' to exit]\nTalk here:")
    if inp.lower() == "quit":
        break
    else:
        print(x.chat(inp))
        
    
