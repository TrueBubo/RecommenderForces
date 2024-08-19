# Recommender Forces
Recommender Forces helps users discover programming problems on Codeforces tailored to their skills and preferences. Leveraging a sophisticated algorithm, it suggests problems closely matching the user's proficiency level while also introducing some novel challenges to keep the experience engaging.

## Key features
  -  Personalized Recommendations: Recommends problems based on user skills and preferences.
 -   Dynamic Recommendations: Balances between closest problems to the user's rating and novel challenges.
-    Multi-user Support: Allows multiple users to be logged in simultaneously.

## Installation
### Using docker
`sudo docker-compose up`

### Manual
To get started with Recommender Forces, ensure you have python3 installed along with the following Python packages (tested versions listed):

`asgiref==3.7.2`
`certifi==2024.2.2`
`charset-normalizer==3.3.2`
`Django==5.0.2`
`djangorestframework==3.14.0`
`idna==3.6`
`jsonfield==3.1.0`
`numpy==1.26.4`
`pytz==2023.3.post1`
`requests==2.31.0`
`sqlparse==0.4.4`
`urllib3==2.2.0`

## User guide
### Running the program
1. Clone the repository
```bash
git clone https://github.com/TrueBubo/RecommenderForces
cd RecommenderForces
```
2. Start the server
```bash
python manage.py runserver
```
3. Access the development server through the provided address.

### Register and login
Click on the "Register" button and enter your Codeforces username. For testing purposes, you can use the username `tourist`.

Login with the same credentials used during registration.

### Rating problems
If you are not on the page where you rate problems, click on the Rate button in header.

There you see problems you have attempted, but not yet rated. To rate the problems use the slider, and move it to the left if you hated the problem, or to the right if you loved it.  Only problems where you chose whether you liked them or disliked them will be submitted. To submit ratings click on the submit button in the bottom-right corner.

1. Navigate to the rating page by clicking on the "Rate" button in the header.
2. Rate problems using the slider. Move it left if you disliked the problem, right if you liked it.
3. Submit ratings by clicking the submit button in the bottom-right corner.

### Recommended problems
Access the recommended problems page by clicking on the "Recommended" button in the header.

Rate problems to receive recommendations tailored to your preferences.

Click on a recommended problem to be redirected to the Codeforces website.

### Force update
If you believe the problem recommendations are outdated, click on the reload button in the header.

Enjoy exploring and solving coding challenges tailored just for you! 
