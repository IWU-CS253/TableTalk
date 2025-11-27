Iteration Report #3
What was each developer responsible for:
Jillian was responsible for finishing the “add to cart” sections of the recipe_card.html and the security breach control for the entire application. This includes protection against SQL injection and password hashing.

Demarco was responsible for starting and developing the unit test for the project.

Keshav was responsible for implementing the appliance filtering feature and separating CSS from HTML files into external stylesheets. 

What was completed:
Jillian completed the cart section of adding new items to carts and keeping carts separately stored in the session section of the application in the “cart” stored section. I also completed a hash password for the database to ensure more secure logins and security of users passwords as well as reformatting the log in sections to add parameters to keep from being vulnerable against SQL injection attacks.

Demarco started the process by creating the file for the unit test, and started working on actually finishing the functions within the file.

Keshav completed the CSS separation by extracting all inline styles from login.html and new_user_sign_up.html into an external static/style.css file for better code organization. He also worked on implementing the appliance filtering system to allow users to view recipes they can make based on the kitchen appliances they own.

What was planned but not finished:
We had planned to have the entire application done by now so we would not have to work over Thanksgiving break, but there is still more work to be done fixing the cart, unit tests.

What trouble/issues/roadblocks we encountered:
One trouble for Jillian was that she couldn’t figure out how to keep separate carts stored in the session variable.

One issue for Demarco was that there was a conflict with the pull request where it was something wrong with the app.py file and somehow the TableTalk.db. There wasn’t any clear reasons why because those files weren’t touched but it had something wrong. It was countered by accepting the version that was inside of the repository and then adding and committing that back into the repository. 



Adjustments to design:
The adjustments Jillian made to the design were that we created a session[‘cart’] storage and then when the user logged out I made an empty place holder and updated the user table with their cart before logging out. This makes it so the user can fetch their cart when logging in and have it updated but not let other users have access or share a universal cart, which was what was happening before.

What tool/process was helpful:
Rewatching the session CS50 video was helpful to understanding how session variables worked and then when having trouble storing the cart and fetching it when users logged in or out I used stackoverflow to learn new methods like json.dump() to be able to edit the values stored without error and then be able to store them again as a json object in the table.

One thing you learned during this iteration:
One thing I learned this iteration was that I can store multiple variables in a session object and how that storing works along with more deeply JSON objects and how to manipulate them and use them meaningfully. 
Plan:
What user stories will you tackle:
I think in the coming week before user testing, development will ramp down but I, Jillian, will try to help with finishing touches making everything runs smoothly and try testing the application with my family at Thanksgiving so I can see how someone who does not know how the application is supposed to work works with it and catch any small errors that are occurring that I am missing.

Keshav will work on implementing a comments feature that allows users to add comments to recipe posts. He will also review the entire application to add CSS styling where necessary to improve the visual consistency and user experience across all pages.

Who will be responsible for what tasks:
Jillian will be responsible for the user profiles and any unfinished work there with making it run as expected and how people interact with the application through user interface and fix any code bugs there. 

Keshav will be responsible for implementing the comments system including backend routes and frontend display on recipe pages. He will also review and update CSS styling across all templates to ensure consistent design throughout the application and also add a few custom css styles.

Demarco will be responsible for finishing the unit testing work and then anything else that needs the assistance.


