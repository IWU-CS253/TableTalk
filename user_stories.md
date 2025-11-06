OFFICIAL TABLETALK USER STORIES

1. As a User, I want to be able to sign up, so that I can post, comment, and contribute to the website.
	The signup field will be on the main page
	To sign up the user must provide:
		A unique username.
		A valid password.
	When the sign up button is clicked the website will validate whether the username or email are already.
	When signed up, username and password pairs will be added to the sql database.
	After a user signs up:
		They are automatically logged in or redirected to the main page to log in.
	A new user profile is created with default settings.
	Users can access and edit their profile settings, can post, comment, and utilize the full websites functionality/
2. As a User, I want to be able to log in, so that I have access to my posts, my  favorite posts, and users I follow.
	The login field will be on the main page.
	Users can log in using their username and password they used to sign up.
	If incorrect information is used to log in an error message will be displayed.
	Once logged in:
		Users can access and edit their profile and settings.
		Users can view, edit, and add to their posts.
	Users will remain signed in until they logout or close all instances of the website open.
3. As a User, I want quick redirection options to ALL available pages.
	Create a fixed navigation bar
	Have options in bar for all available pages (cart, main feed, user profile)
	On a click redirect the user to that rendered html file
	Use app.py file to create all the route possible for users to take
4. As a User, I want to be able to post recipes, so that other users can make them and comment on them.
	Users can post a new recipe by clicking the make a new post button.
	A recipe post must include:
		A title
		An ingredient list
		Step by step instructions
		The appliances required
		The estimated cook time
	Users can edit and delete their posts.
	After posting, the recipe is added to both the main feed and the user’s profile.
5. As a User, I want to be able to upload images of my recipe so people can view.
	Click “Upload Image” button
	Use a software which allows device image upload
	Specify which image you want to post
	Make sure image type is supported and in appropriate size
	Click “Post” button
	Make sure all fields are filled in and make image optional
6. As a User, I want to see my own recipes.
	In the user’s profile, a list of all their recipe cards
	Available drop down to search or filter their own posts (with same set up as above)
	At top of their profile have a live count attribute of how many recipes they have on their profile
	If they have no recipes, leave a prompt saying “Start by posting your first recipe now!” 
7. As a User, I want to be able to filter through posts, so that I can find which recipes I want to make or save.
	A search bar will be on a persistent header bar above the posts feed.
	Users can search posts by:
		The recipe name.
		Ingredients it contains.
		The name of the user who posted it.
		Appliances needed or food types.
	Search results display posts that fit the search sorted by relevance or recency.
	Users can click on a result to bring them to the post.
8. As a User, I want to be able to select the appliances and materials I own, so that I can filter posts that I can make with what I have.
	Users can list their appliances and materials in their profile settings.
	Posts are tagged with the appliances and materials needed to make the recipe.
	The by default in the search filter, recipes requiring unavailable equipment are hidden.
	Users can update their appliances at anytime.
9. As a User, I want to be able to comment on posts, so that I can give feedback and recommendations to the poster.
	Each post includes a comments section.
	Users must be logged in to comment.
	Comments display the username, message, and time it was made.
	All logged in users can reply to or like comments.
	Users can edit and delete their own comments.
10. As a User, I want to be able to follow and friend other users, so that I can see and stay up to date on new recipes they post.
	A follow button can be found on user profiles.
	Following a user adds their posts to the follower’s feed.
	Users who follow each other are friends.
	Notifications are sent when followed users post new recipes or comment on your post.
11. As a User, I want to enter a “cook” mode that I can follow easy step-by-step instructions while cooking
	When clicking “Cook” button text enlarges and hides other elements of the page (most commonly in a popup)
	Only displays one step at a time.
	Users can navigate between steps with a “next” and “back” button.
12. As a Creator, I want to implement the Instacart API available so users can use the car list to directly make an InstaCart order.
	Research InstaCart API
	Store and imbed the API in the cart tab so it keeps the same familiar look as the previous application set up
	Allow users when they press “Cook It!” to add all ingredients to an InstaCart order rather than their cart list
13. As a User, I want to be able to save the ingredients of a recipe, so I know what I have to buy at the store, but keep the ingredients for each recipe separated so I can prioritize the recipes I want to make most.
	Each recipe card has a “Cook It” button which saves ingredients to the shopping cart
	The shopping list is categorized as an ordered list to specify how many recipes I have saved
	Within each ordered list element, there will be an embedded unordered list with all the ingredients per recipe
	Each ordered recipe item can be expanded or collapsed as well as deleted
	Each unordered item can be deleted to symbolize  purchasing that item at the store
	Make sure the cart is updated in real time on the user’s screen
