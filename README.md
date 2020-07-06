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
> The library contains two classes, one for `user data` and one for `network data`
> The library first has to be imported, and then we have to set path to the experiment round we want to analyse 
> Numerical `user ID` corresponds to `node ID` in `NetworkX`

```python 
import experiments_data as ed

ed.data_location("experiments_ES/first_run/round1/") 

user_data = ed.user_data() # this is data about users and behaviour
network_data = ed.network_data() # data about the network

'''
Some function have default parameters of None, and they will return a full list of actions,
where others might require username or user ID, which is numerical 
'''

```

---

## Documentation


---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://nutmeg.social" target="_blank">NUTMEG</a>.