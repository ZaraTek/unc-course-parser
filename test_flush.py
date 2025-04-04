import os
import time

for i in range(0, 1000):
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(i, flush=True)
    time.sleep(0.1)  # optional delay so you can actually see it change
