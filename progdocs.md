# Recommender Forces Documentation
## About
This documentation provides an overview of the Recommender Forces project, detailing its file structure and inner workings. While this document aims to clarify the organization and functionality of the project, for detailed insight into the program's operations, it is recommended to refer directly to the source code.

## Project organization
### Apps 
The project consists of the following apps:
- api: Facilitates direct interaction with the database through a browser, primarily designed for accessing public data.
- problems: Manages all functionalities related to interaction with problems
- users: Responsible for user management, including creation, authentication, and association with problems.

### File organization
The project adheres to the Model-View-Controller (MVC) architecture:

**Model**: Defines data representation in the database and is implemented in `models.py`.
**View**: Manages the HTML files presented to users, stored in the `templates` directory of each app.
Controller: Handles data logic. It can be found in views.py

Additionally, a utility file named `helpful_functions.py` is included for housing miscellaneous functions.

## Important functions
### users/view.py/register
- Handles post `GET` and `POST` requests
- Renders the register page for GET requests.
- Performs verification of submitted details and registers the user in the database for `POST` requests.

### problems/views.py/update_problems
- Retrieves problems from the Codeforces API and stores them locally in the database.
- Enhances website loading speed by reducing the need for frequent external API requests.

### problem/views.py/rate
- Manages the rating page, displaying problems attempted but not yet rated by the logged-in user.
- Updates user preferences based on the topics of rated problems.
- User preferences for a topic are set as the average rating of all rated problems with such topic.
- Rating for a topic can range from -2 when the user hated all problem with that topic, up to 2, when they loved all such problems
- Ratings for a topic are saved as the sum of all ratings and the number of all ratings, allowing easy calculation of averages. 

### problem/views.py/recommend
- Implements the recommendation page, presenting unattempted problems to the user.
- Determines problem similarity based on average ratings of problems with similar tags.
- Similarity of a problem is calculated using the Euclidian distance between user preferences and topics of a problem. 
This distance is then normalized for the number of topics. You can read more about it in helper_functions.py/euclidian_distance_squared_per_component documentation
- The similarity of a problem can be thought of as the similarity between user and another user who only rated this problem, and also loved the problem
- Selects a random sample of closest problems, with selection probability decreasing for less similar problems.

###  helper_functions.py/euclidian_distance_squared_per_component
- Finds squared Euclidian distance between a new problem and current likings of the user. 
- To save computation distance is squared to avoid unnecessary sqrt function calls. 
- Utilizes a per-component measure to address the potential disadvantage of problems with more tags.
- Only compares topic distance if user already rated problems with such topic. Otherwise, it would disadvantage new 
topics as this distance would increase distance from baseline, which is no information (represented as 0)

### helper_functions.py/k_smallest_elements
- Retuns $k$ smallest elements based on `euclidian_distance_squared_per_component`. 
- Uses algorithm similar to quickselect for efficient computation.

## Important external libraries 
### Numpy
`Numpy` was used for data analysis to speed computations compared to stock python
### Requests
Used for retrieving data from Codeforces API