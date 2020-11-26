# Dog Adoption Scrape

The website https://labsandmore.org/dogs/ uploads dogs in California that are up for adoption. The problem is the waitlist fills up extremely fast and there's no notification system or email list. Thus I've been called to duty to scrape the website every hour and send a text when new dogs have been found for my friend looking to adopt!

I use the package Selenium to scrape the website, Pandas for some of the minor data wrangling, and finally Yagmail to send the text (from email).

The Jupyter Notebook was used to build up the script from which I then essentially just copy-pasted over the cells to an actual .py file. I then created a batch script which runs the .py file and finally created a Task on Windows Task Scheduler that runs the batch script running the Python script every hour every day from 10am to 8pm (only sending texts when new dogs are found). You can find the Notebook above which details all the steps, the .py file with all the guts, my simple batch script running it all, as well as some screenshots from Task Scheduler on how I set up the Task inside the screenshots folder.    

An example text is shown below:

![alt text](https://i.ibb.co/HC9BFMk/Text-Screenshot.png)  
(Note: The Husky "Artichoke" had many pups all uploaded at the same time in case that data looked off to you!)
