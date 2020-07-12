<a href="http://fvcproductions.com"><img src="https://i.ibb.co/wrVMjTr/nutmeg.png" width="200px" title="NUTMEGlogo" alt="NUTMEGlogo"></a>

***NUTMEG: Network Evaluation Multiplayer Game for studying contagion processes on networks***

# NUTMEG Analysis Library

> experiments_data.py contains all the methods

> Sample usage under sample_use.py


**Dependencies**

- Pandas
- NetworkX 

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) [![Generic badge](https://img.shields.io/badge/release-1.0-blue.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/NetworkX-2.1-blue.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/pandas-0.23.4-blue.svg)](https://shields.io/)


- With the library you can get information about the user behaviour and the network 
- Sample of data collected in Spain avaliable under experiments_ES

> User Data

- Get ID from username 
- Get username from ID
- Check if user is seed 
- Check if user got infected in the round
- Get a list of infected nodes 
- Get list of actions for given user, which can also return certain actions at given timestep
- Get actions of users before and after they got infected
- Convert data from XML to pandas dataframe 
- Get list of interactions between two nodes throughout the whole round 

> Network Data

- Get list of edges
- Get status of each node at given timestep
- Convert data to NetworkX object
- Check if two users are connected 
- Plot the network
- Animate the actions, to recreate what happened during the experiment

**Animation Example**

![Recordit GIF](https://i.ibb.co/R9k2Gxs/ezgif-5-24c13b369335.gif)

---

## Table of Contents

- [Usage](#usage)
- [Documentation](#documentation)

---

## Example

```python 
''' check the actions of a specific user before they got infected, using their username '''

import experiments_data as ed

ed.data_location("experiments_ES/first_run/round1/") # set path to the experiment

user_data.actions_before_infection(username="Anna") # pass in the username as parameter without XML extension

# The function returns a list of all the actions user took before they got infected
['block', 'block', 'received', 'sent', 'opened_item', 'received', 'deleted', 'received', 'deleted', 'sent', 'sent', 'sent', 'received']

```

---

## Usage
> The library contains two classes, one for `user data` and one for `network data`.
> The library first has to be imported, and then we have to set path to the experiment round we want to analyse.
> Numerical `user ID` corresponds to `node ID` in `NetworkX`.

```python 
import experiments_data as ed

ed.data_location("experiments_ES/first_run/round1/") 

user_data = ed.user_data() # this is data about users and behaviour
network_data = ed.network_data() # data about the network

'''
Some function have default parameters of None, and they will return a full list of actions,
where others might require username or user ID, which is numerical 
'''

user_data.user_infected_in_round(user_id=7) # simple function to tell you if a user was infected in the round, you can use either user ID or username
>>> True
user_data.user_is_seed(username="roco89") # check if user was a seed, the parameter is also either username or user ID 
>>> False
```

---

## Documentation
> The avaliable functions, parameters and return types.
> Each experiment took 60 seconds, so the timesteps avaliable to extract data are from 0 to 59 

- Scikit-learn Function

> Sample features avaliable in experiment_features.csv

```python
import experiments_data as ed

ed.data_location("experiments_ES/first_run/round1/") 

>>> ed.generate_action_csv() 
Actions in CSV: ['sent', 'received', 'opened_item', 'deleted']


	'''
		The function will generate a CSV file from the actions in the scenario, to which the path location is set to
		Once file has been generated, the actions that have been found, will be shown in the console
		The CSV file which can be lodaded in to sklearn has the following format (if all 4 features are used):
		            Column 1          Column 2          Column 3      Column 4
		row1	number_of_samples, number_of_features,   class0,       class1
		
		row2       number_sent         no_received    no_opened_item  no_deleted
		 .
		 .
		 .
	   row n
	'''

```

- Network Data Functions

```python 
get_edgelist()
	'''
	Takes no parameters
	:return: return a list of tuples between each nodes
	'''
	return edge_list

>>> get_edgelist()
[(7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 18), (7, 21), (7, 22), (8, 9)]

plot_round_network()
	'''
	Takes no parameters
	Doesn't return an object
	Used to show a plot of the network (without any status)
	'''


animate_network()
	'''
	Takes no parameters
	Doesn't return an object
	Shows an animation of the experiment, with each node changing colour depending on its status
	Green - Healthy node without any infected messages
	Yellow - Node has received an infected message but not opened it
	Red - Infected by a message that was opened 
	'''

network_status_at_time(timestep)
	'''
	Takes an integer timestep parameter, corresponding to a given second in the experiment 
	:param timestep: timestep in seconds from 0 to 59
	:return: return a list of nodes with their status at each time t
	'''
	return status_list

>>> network_data.network_status_at_time(10)
[{'7': 'exposed'}, {'8': 'infected'}, {'9': 'exposed'}, {'10': 'exposed'}, {'11': 'healthy'}, {'12': 'healthy'}, {'13': 'healthy'}]
		
to_networkx_object()
	'''
	Takes no parameters
	Returns networkX object 
	:return: networkX object of the graph
	'''
	return graph

users_connected(s, t)
	'''
	Takes two integer parameters, user ID 1 and user ID 2
	:param s: source node
	:param t: target node
	:return: boolean if two nodes are connected
	'''
	return user_connected
	
get_neighbours(user_id, username):
	'''
	Return a list of neighbours of a node with a given ID or username, if both blank will return an error

	:param user_id: numeric ID of a node
	:param username: username of a node
	:return: list of neighbours
	'''
	return list_of_neighbours
	
>>> network_data.get_neighbours(user_id=9)
[8, 11, 14, 16, 17, 20, 22
```

- User Data Functions 

```python 
get_id_from_username(username)
	'''
	Takes string parameter of the username, which is the name of the XML file without the extension 
	:return: return a user ID integer 
	'''
	return user_id

>>> user_data.get_id_from_username("Pablo")
11 

get_username_from_id(user_id)
	'''
	Takes integer parameter of the user ID, this is the same as node ID in the graph
	:return: return a username string
	'''
	return username
	
>>> user_data.get_username_from_id(15)
Oxyura

user_is_seed(user_id=None, username=None)
	'''
	Function takes either numerical user ID used in the tracking files, or username
	and checks if the user was infected during given round
	:param user_id: numerical user ID
	:param username: String username
	:return: boolean value
	'''
	return user_seeded
	
>>> user_data.user_is_seed(user_id=14)
True 
>>> user_data.user_is_seed(username="raquel")
False

user_infected_in_round(user_id=None, username=None)
	'''
	Doesn't take into account if the user was seed, but will return a boolean value if user was infected in the given round
	:param user_id:
	:param username:
	:return: bolean
	return infected_in_round
	
>>> user_data.user_infected_in_round(username="Anna")
False
>>> user_data.user_infected_in_round(user_id=13)
True

list_of_infected()
	'''
	Takes no parameters
	Returns a list of user IDs which have been infected 
	:return: list of all user_ids infected in the round
	'''
	return list_of_infected_nodes

>>> list_of_infected()
[7, 8, 9, 11, 12, 13, 15, 16, 19, 20]

list_of_actions(user_id=None, username=None, timestep=None)
	'''
	If no parameters are passed, the function will return all actions at each timestep
	With user_id or username parameter, the function will return interactions from a specific user
	timestep parameter will get all the actions at a given timestep

	:param user_id: numerical user ID
	:param username: String username
	:param timestep: time t at which all actions occured
	:return: list of actions
	'''
	return actions_dict

>>> user_data.list_of_actions()
{1592904524: None, 1592904525: ['received', 'sent', 'sent', 'sent', 'received', 'received'], 1592904526: ['received', 'sent', 'received', 'received', 'sent', 'sent'], 1592904527: ['received', 'sent', 'sent', 'sent', 'received', 'received'].....}

>>> user_data.list_of_actions(username="Anna")
{1592904524: None, 1592904525: None, 1592904526: None, 1592904527: None, 1592904528: None, 1592904529: ['received'], 1592904530: None, 1592904531: ['sent'].....}

>>> user_data.list_of_actions(timestep=10)
{1592904534: ['sent', 'deleted', 'received', 'sent', 'received', 'sent', 'opened_item', 'sent', 'deleted', 'received', 'received']}

>>> user_data.list_of_actions(username="Anna", timestep=10)
{1592904534: None}

actions_before_infection(user_id=None, username=None)
	'''
	Takes either numerical user ID or string username, if nothing passed it will amalgamate all user actions 
	Returns a list of actions that took place before infection 
	:param user_id: numerical user ID
	:param username: String username
	:return: If no parameters passed, return actions before infection for all users, otherwise return for specific user
	'''
	return action_list

>>> user_data.actions_before_infection()
['sent', 'deleted', 'received', 'deleted', 'sent', 'sent', 'sent', 'sent', 'received', 'block', 'block', 'received', 'sent', 'opened_item', 'received', 'deleted', .....]

>>> user_data.actions_before_infection(user_id=11)
['received', 'deleted', 'sent']

>>> user_data.actions_before_infection(username="mttll")
['sent', 'sent', 'sent', 'sent', 'sent', 'sent', 'sent', 'received', 'sent', 'sent', 'received', 'received', 'opened_item']

actions_after_infection(user_id=None, username=None)
	'''
	Takes either numerical user ID or string username, if nothing passed it will amalgamate all user actions 
	Returns a list of actions that took place before infection 
	:param user_id: numerical user ID
	:param username: String username
	:return: If no parameters passed, return actions after infection for all users, otherwise return for specific user
	'''
	return action_list
	
***SAME USAGE AS ABOVE***

infection_dataframe(filename)
	'''
	Takes in the XML filename we want to convert to pandas dataframe
	convert the XML file into a pandas dataframe, with information about each timestep and infection of the given user/file at each time t
	:param filename: filename of the XML we want to convert
	:return: df
	'''
	return infection_dataframe

>>> df = user_data.infection_dataframe(filename="elenita.xml")

interactions_between_nodes(user_id_a, user_id_b)
	'''
	Takes in the numerical ID of two nodes, which we want to get the interactions between
	Returns two dictionaries, which act as a timeline for the two users, and the actions they took at each time step 
	:return: dict_a, dict_b
	'''
	return node_a_actions, node_b_actions
	
>>> node_a, node_b = user_data.interactions_between_nodes(node_a, node_b)
>>> node_a
{1592904524: None, 1592904525: None, 1592904526: None, 1592904527: ['received'], 1592904528: ['sent'], 1592904529: None, 1592904530: None .....}
>>> node_b
{1592904524: None, 1592904525: None, 1592904526: None, 1592904527: ['sent'], 1592904528: ['received'], 1592904529: None, 1592904530: None .....}

count_action(list_of_actions=None, action_type=None)
	'''
	The function takes in the list of actions from the interactions_between_nodes or list_of_actions functions and counts either all of the actions or a specific action type
	:param list_of_actions: the dict returned by interactions_between_nodes() or list_of_actions() function
	:param action_type: String value, if you want to count a specific action e.g. "opened_item"
	:return: a dict with counted values
	'''
	return count_action_dict
	
user_a, user_b = user_data.interactions_between_nodes(7, 13) # get interactions between two nodes first 

>>> user_data.count_action(a)
Counter({'sent': 3, 'received': 2})

>>> user_data.count_action(b, action_type="opened_item") # count specific action type - types avaliable: "sent", "received", "opened_item", "deleted"
{'opened_item': 1}


list_of_actions = user_data.list_of_actions(user_id=12) # can also use the list_of_actions() function for a single user
>>> user_data.count_action(list_of_actions)
Counter({'sent': 24, 'received': 15, 'opened_item': 9, 'deleted': 4})

interacted_in_scenario(user_id_a, user_id_b):
        '''
        Check if two users interacted with each other during the scenario
        :param user_id_a: source node numeric ID
        :param user_id_b: target node numeric ID
        :return: boolean, True if the two interacted, False if they didn't
        '''
		return interacted_bool

>>> user_data.interacted_in_scenario(7, 9)
False 
```

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://nutmeg.social" target="_blank">NUTMEG</a>.