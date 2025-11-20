Iteration Report #2
What was each developer responsible for:
Jillian was responsible for setting up the main feed page where it displayed all posts from the database into the main feed section as well as the friends aside section where all the friends, not including your own account, be displayed on the side where the logged in user can add friends and view friend’s profiles. She also started implementing the large view of recipes and adding recipes to the cart. This is not yet finished but will be by next week.

Emory was responsible for setting up the backend for appliances. He was responsible for making the SQL table for appliances, making the app route for adding appliances while editing a user profile, as well as the app route for adding appliances to posts. He also connected the navigation bar buttons with their corresponding app routes.

Keshav was responsible for setting up the frontend of appliances  trying  to connect the appliances with the ids from the user table so that it displays under each profile. I am also working on finishing separating the css files from the html.

Demarco was responsible for editing  the code within the recipe_card.html and user_profile.html files to actually pull from the database. Instead of having all placement holders within the code. Also, any new routes for functionality relating to this change was done as well. This may need to be checked but it will be done by next week. 

What was completed:
The main feed implementation was finished and committed to the remote repository. This has fixed bugs in the posting of recipes going alongside the filtering of recipes on the mainfeed without auto triggering different filter attributes. Backend appliance functionality was completed. Navigation bar button functionality was finished. 

What was planned but not finished:
One thing that was planned but not yet finished is the cart site page. This does not yet currently display the items in the cart in a list form. We want to have this finished as well as implement the idea that a recipe can not be added to a cart more than once. We also want to make sure that if a recipe is deleted, the recipe can still be displayed in the cart without breaking the interface. Frontend appliance functionality was not finished. 

What trouble/issues/roadblocks we encountered:
One problem that Jillian encountered this week was that when she implemented the filter posts section, when the label for a recipe was changed on a new post it would auto trigger the filter for main feed posts. This would disregard all the entries trying to be made and submit would never actually happen. 

One problem Demarco faced was dealing with committing the work but then there would be a conflict with the code. Ultimately the code would be erased locally to his computer but then he would have to replace it. Also, the routes for the functions inside of app.py was slightly wrong which was causing errors.

Adjustments to design:
One adjustment to this design would be to filter the posts and labels from two different dropdowns. This made it much easier to filter separately without on change triggers happening prematurely.

What tool/process was helpful:
One tool or process that was helpful was every time something was changed, I would run my local program and make sure it worked and looked how I wanted it to work. This was tedious but very helpful to see what I was actually working on and changing in small increments without unknowingly breaking the entire program. 

One thing you learned during this iteration:
One thing Jillian learned was how to test code on my personal computer and text it each time changes were made. I also found it helpful to ask other people to try my code from someone who does not know how the code is supposed to work. This helps me see how users are unknowingly interacting and forcing changes to the program. I also learned about data-labels to separate uses in my dropdowns and the filtering process.

Emory learned that you can access a different table value depending on user input on one line of code.
Plan:
What user stories will you tackle:
Jillian will try to tackle the user interactions with the cart and recipe large view styles. Although there is not a user story for the security of the website, I want to accomplish this before user testing day to have a secure environment for users to trust and interact with.  

Emory will try to tackle the user following and friending.

Demarco will attempt to finish the unit testing work.

Keshav will try to work on Adding comments to posts and implementing cook mode feature.

Who will be responsible for what tasks:
Jillian will be responsible for working in security measures like encrypting the passwords in the users table with a hash function. I also want to work on defending SQL injections into the login pages. I will also work on finishing the cart and “Cook It” button features to finish the wireframe of the entire project. 

Emory will be responsible for implementing the backend friending and following functionality.

Demarco will be responsible for writing unit tests.

Keshav will be working with implementing the backend and frontend for the cook mode feature along with adding a feature of comments in posts.
