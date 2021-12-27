# auto-ct
Automates doing Chloe Ting challenges with selenium (has options for tracking progress and setting up music, supports all challenges released thus far)

# How to run this
After you have ensured that a python interpreter exists and while in the folder containing your source files, type python3 setup.py

NOTE: If you dont have much experience with github, go to the 'text' folder in this repository and read 'setup.txt'

# setup.py / workout.py
Anyway, running setup.py will begin the setup process, follow the prompts onscreen

When you finish setting up, you can begin your chosen challenge by running workout.py (type python3 workout.py)

Running workout.py will open your videos for the day and open music as well if you specified it in setup. As you finish each video (or if you are otherwise done with it), you can continue on to the next video through a prompt in the terminal (your current video will be closed and the next will be opened. if applicable, your music tab will stay open)

workout.py is meant to be run every day you do the challenge

# More automation
You can conveniently automate running workout.py if you want by setting a cronjob (Linux/MacOS) or configuring a task using Task Manager (Windows) to run the program at a specific time everyday. You can also create an alias in ~/.bashrc to execute the file when you type a short command so you dont have to navigate to the folder and type the command each time (for example: alias wkpy="cd ~/py-execs/workout/auto-ct-main && python3 workout.py")

Some flags are supported for customization (python3 workout.py --help) but I would recommend just doing a satisfactory job setting defaults in setup.py (or if necessary, changing small things directly in the config file 'envb.py')

Thanks for running, good luck!
=======
Automates doing Chloe Ting challenges with selenium (has options for tracking progress and setting up music, supports all challenges released thus far) 
>>>>>>> 33302243b83705194d9cf3e625dc80ad10a86eb7
