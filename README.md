# MyBib

Keep track of your bibliography using Neo4j. With a simple user interface add research papers from their BibTex citations, query them and link them together.

## Deploy to Heroku:

Simply follow the [steps outlined here](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app), but instead of cloning their source code, clone this repository instead (`https://github.com/fferegrino/mybib.git`).  

You'll also need a running instance of Neo4j, I used [GrapheneDB](https://elements.heroku.com/addons/graphenedb), which is free and easy to install into your recently created Heroku app.  

After deployment, there are two configurations that you must set in order to interact with your app: `MYBIB_USER` and `MYBIB_PASS`, these values will be used for authentication.
