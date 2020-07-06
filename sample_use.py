import experiments_data as ed

ed.data_location("experiments_ES/first_run/round1/") # set the location of which round you want to analyse,
# I will create a table for this, saying which scenario was ran on which network, similar to what I've sent you before

user_data = ed.user_data() # this is data about users and behaviour

# The messages are passed using user ID's and not usernames
# usernames are the xml files
# You can use a couple of functions to either get user ID using username or vice versa

user_id = user_data.get_id_from_username("Anna") # get user ID from username
username = user_data.get_username_from_id(9) # get username from ID

print (username)

# using this function you can get all the actions performed by the user before they got infected as a list
# you can pass in either user ID or username as a parameter
print (user_data.actions_before_infection(username="Anna"))

# same thing for what the user did after they got infected
print (user_data.actions_after_infection(user_id=user_id))

'''
If you don't pass any user parameters to the functions above, by default it will return list of actions before and after for all users amalgamated 
'''

print (user_data.infection_dataframe("Pablo.xml")) # this will return you a pandas dataframe for the XML file, which tells you about the infection status at each timestep,
# that is if the message is infected and the user is infected at each time

print (user_data.user_infected_in_round(user_id=7)) # simple function to tell you if a user was infected in the round, you can use either user ID or username

print (user_data.user_is_seed(username="roco89")) # check if user was a seed

print (user_data.list_of_infected()) # a list of user IDs, who got infected in the round

network_data = ed.network_data() # data about the network

print (network_data.get_edgelist()) # returns a tuple of list of edges

graph = network_data.to_networkx_object()

# network_data.plot_round_network() # plots the network graph
# network_data.animate_network() # recreate what happened during the experiment as an animation