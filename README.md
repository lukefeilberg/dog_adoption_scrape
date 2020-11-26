# Dog Adoption Scrape

The website https://labsandmore.org/dogs/ uploads dogs in California that are up for adoption. The problem is the waitlist fills up extremely fast and there's no notification system or email list.

Thus I've been called to duty to scrape the website every hour and send a text when new dogs have been found for my friend looking to adopt!

I use the package Selenium to scrape the website, Pandas for some of the minor data wrangling, and finally Yagmail to send the text (from email).

This notebook was used to build up the script from which I then essentially just copy-pasted over the cells to an actual .py file. I then created a batch script which runs the .py file and finally created a Task on Windows Task Scheduler that runs the batch script running the Python script every hour every day from 10am to 8pm (only sending texts when new dogs are found).
