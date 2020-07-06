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
```

- User Data Functions 

```python 
get_id_from_username(username)
get_username_from_id(user_id)
user_is_seed(user_id=None, username=None)
user_infected_in_round(user_id=None, username=None)
list_of_infected()
list_of_actions(user_id=None, username=None, timestep=None)
actions_before_infection(user_id=None, username=None)
actions_after_infection(user_id=None, username=None)
infection_dataframe(filename)
interactions_between_nodes(user_id_a, user_id_b)
```

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://nutmeg.social" target="_blank">NUTMEG</a>.