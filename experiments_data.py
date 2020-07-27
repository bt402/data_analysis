import xml.etree.cElementTree as et
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
import pathlib
from collections import Counter
import numpy as np
import os
import ntpath

path_ = None
f_count_ = None
file_arr_ = None
no_of_files_ = None

def data_location(path):
    global path_, f_count_, file_arr_, no_of_files_
    path_ = path

    f_count_ = 0
    parent_dir = pathlib.Path(path)
    file_arr_ = list(glob.iglob(str(parent_dir.parent) + '/status/*_status.csv'))
    no_of_files_ = len(file_arr_)

def get_action_types():
    all_files = glob.glob(path_ + "*.xml")

    a_counter = Counter()
    for f in all_files:
        username = f.strip().split("\\")[1].split(".")[0]
        ud = user_data()
        a_counter = a_counter + ud.count_action(ud.list_of_actions(username=username))

    original_list = ["sent", "received", "opened_item", "deleted"]
    scenario_list = list(a_counter.keys())

    main_list = np.setdiff1d(original_list, scenario_list)
    if len(main_list) > 0: # if there is an action that doesn't exist, remove it from the original
        for m in main_list:
            original_list.remove(m)

    return original_list

def generate_action_csv():
    file = open(path_ + "experiment_features.csv", "w+")

    all_files = glob.glob(path_ + "*.xml")

    actions_performed = get_action_types()

    file.write(str(len(all_files)) + "," + str(len(actions_performed)) +  ",healthy,infected" + "\n")

    lines = ""

    for f in all_files:
        username = f.strip().split("\\")[1].split(".")[0]
        ud = user_data()
        l = dict(ud.count_action(ud.list_of_actions(username=username)))
        line = ""
        for action in actions_performed:
            ua = l.get(action)
            if ua != None:
                line += str(ua) + ","
            else:
                line += "0" + ","
        lines += line[:-1] + "," + str(int(ud.user_infected_in_round(username=username))) + "\n"
        # print (ud.count_action(ud.list_of_actions(username=username)), ud.user_infected_in_round(username=username))
    file.write(lines[:-1])
    file.close()
    print ("Actions in CSV:" , actions_performed)

class network_data:

    def timestep_list(self):
        parent_dir = pathlib.Path(path_).parent
        status_files = list(glob.iglob(str(parent_dir) + '/status/*_status.csv'))
        t_list = []

        for file in status_files:
            timestep = file.split("\\")[2].split("_")[0]
            t_list.append(int(timestep))

        t_list.sort()

        return t_list

    def get_color_map(self, filename):
        f = open(filename)
        d = {}
        for line in f:
            node_color = line.strip().split(",")
            node = int(node_color[0])
            color = node_color[1]
            d.update({node: color})
        return d

    def simple_update(self, num, layout, G, ax):
        global f_count_
        ax.clear()

        # Draw the graph with random node colors
        if f_count_ < no_of_files_:
            val_map = self.get_color_map(file_arr_[f_count_])
            c_map = []
            for n in G.nodes():
                v = val_map.get(int(n))
                if v != None:
                    c_map.append(v)
            nx.draw(G, pos=layout, node_color=c_map, ax=ax, with_labels=True)

            # Set the title
            ax.set_title("Time t = {}".format(num))
            f_count_ += 1
        elif f_count_ >= no_of_files_:
            f_count_ = 0


    def get_edgelist(self):
        '''
        :return: return a list of tuples between each nodes
        '''
        edge_list = []

        file = path_ + "graph.edgelist"
        f = open(file)

        for line in f:
            l_split = line.split(" ")
            node_a = int(l_split[0])
            node_b = int(l_split[1])
            edge_list.append((node_a, node_b))

        return edge_list

    def plot_round_network(self):
        '''
        Plot the network from the round
        :return: Void
        '''
        fig, ax = plt.subplots(figsize=(6, 4))

        # Create a graph and layout
        G = nx.read_edgelist(path_ + "graph.edgelist")

        layout = nx.spring_layout(G)

        nx.draw(G, pos=layout, ax=ax, node_color='#00b4d9', with_labels=True)

        plt.show()


    def animate_network(self):
        # Build plot
        fig, ax = plt.subplots(figsize=(6, 4))

        # Create a graph and layout
        G = nx.read_edgelist(path_ + "graph.edgelist")
        n = G.number_of_nodes()
        layout = nx.spring_layout(G)

        ani = animation.FuncAnimation(fig, self.simple_update, frames=no_of_files_, interval=200, fargs=(layout, G, ax))
        ani.save('animation_1.gif', writer='imagemagick')

        plt.axis('off')
        plt.show()

    def network_status_at_time(self, timestep):
        '''

        :param timestep: timestep in seconds from 0 to 59
        :return: return a list of nodes with their status at each time t
        '''
        timestep_list = self.timestep_list()

        parent_dir = pathlib.Path(path_).parent

        # 00FF00 - healthy
        # FF0000 - infected
        # F4DC42 - exposed
        status_list = []

        f = open(str(parent_dir) + "/status/" + str(timestep_list[timestep]) + "_status.csv")
        for line in f:
            node_id = line.strip().split(",")[0]
            status = line.strip().split(",")[1]
            if status == "#00FF00":
                status_list.append({node_id : "healthy"})
            elif status == "#FF0000":
                status_list.append({node_id: "infected"})
            elif status == "#F4DC42":
                status_list.append({node_id: "exposed"})

        return status_list

    def to_networkx_object(self):
        '''
        :return: networkX object of the graph
        '''
        return nx.read_edgelist(path_ + "graph.edgelist")

    def users_connected(self, s, t):
        '''

        :param s: source node
        :param t: target node
        :return: boolean if two nodes are connected
        '''

        G = self.to_networkx_object()
        return str(s) in G.neighbors(str(t))

    def get_neighbours(self, user_id=None, username=None):
        '''
        Return a list of neighbours of a node with a given ID or username, if both blank will return an error

        :param user_id: numeric ID of a node
        :param username: username of a node
        :return: list of neighbours
        '''
        if user_id == None and username == None:
            raise Exception("Username parameter blank")
        elif username != None:
            ud = user_data()
            node = user_data.get_id_from_username(ud, username)
        elif user_id != None:
            node = int(user_id)

        edges = self.get_edgelist()

        nodes_neighbours = []
        for e in edges:
            target, neighbour = e
            if target == node:
                nodes_neighbours.append(neighbour)

        return nodes_neighbours

class user_data:

    def split_id(self, id, index):
        return int(id.strip().split("_")[index])

    def getvalueofnode(self, node):
        """ return node text or None """
        return node.text if node is not None else None

    def update_dict(self, action_dict, f, user_a_id=None, user_b_id=None):
        parsed_xml = et.parse(f)
        for node in parsed_xml.getroot():
            if node.find('blocked_user') == None and node.find('method') == None:
                if node.find('user_infected') != None:
                    if node.find('user_infected').text != None:
                        if node.attrib.values():  # check if actions empty
                            t = int(list(node.attrib.values())[0].split("_")[2])

                            user_a = int(list(node.attrib.values())[0].split("_")[0])
                            user_b = int(list(node.attrib.values())[0].split("_")[1])

                            i_list = [user_a, user_b]

                            if user_a_id != None and user_b_id != None:
                                action = node.tag
                                if user_a_id in i_list and user_b_id in i_list:
                                    if t in action_dict:
                                        curr_val = action_dict.get(t)
                                        if curr_val == None:
                                            action_list = [str(action)]
                                            action_dict[t] = action_list
                                        else:
                                            curr_val.append(str(action))
                                            action_dict[t] = curr_val
            elif node.find('blocked_user') != None:  # blocked action
                if node.attrib.values():  # check if actions empty
                    t = int(list(node.attrib.values())[0].split("_")[2])

                    user_a = int(list(node.attrib.values())[0].split("_")[0])
                    user_b = int(list(node.attrib.values())[0].split("_")[1])

                    i_list = [user_a, user_b]

                    if user_a_id != None and user_b_id != None:
                        action = node.tag
                        if user_a_id in i_list and user_b_id in i_list:
                            if t in action_dict:
                                curr_val = action_dict.get(t)
                                if curr_val == None:
                                    action_list = [str(action)]
                                    action_dict[t] = action_list
                                else:
                                    curr_val.append(str(action))
                                    action_dict[t] = curr_val
            elif node.find('method') != None:  # recover action
                if node.attrib.values():  # check if actions empty
                    t = int(list(node.attrib.values())[0].split("_")[2])

                    user_a = int(list(node.attrib.values())[0].split("_")[0])
                    user_b = int(list(node.attrib.values())[0].split("_")[1])

                    i_list = [user_a, user_b]

                    if user_a_id != None and user_b_id != None:
                        action = node.tag
                        if user_a_id in i_list and user_b_id in i_list:
                            if t in action_dict:
                                curr_val = action_dict.get(t)
                                if curr_val == None:
                                    action_list = [str(action)]
                                    action_dict[t] = action_list
                                else:
                                    curr_val.append(str(action))
                                    action_dict[t] = curr_val
        return action_dict

    def update_action_dict(self, action_dict, f):
        # parsed_xml.find("received").attrib['message_id']
        parsed_xml = et.parse(f)
        for node in parsed_xml.getroot():
            if node.find('blocked_user') == None and node.find('method') == None:
                if node.find('user_infected') != None:
                    if node.find('user_infected').text != None:
                        if node.attrib.values():  # check if actions empty
                            t = int(list(node.attrib.values())[0].split("_")[2])
                            action = node.tag
                            if t in action_dict:
                                curr_val = action_dict.get(t)
                                if curr_val == None:
                                    action_list = [str(action)]
                                    action_dict[t] = action_list
                                else:
                                    curr_val.append(str(action))
                                    action_dict[t] = curr_val
            elif node.find('blocked_user') != None:  # blocked action
                if node.attrib.values(): # check if actions empty
                    t = int(list(node.attrib.values())[0].split("_")[2])
                    action = node.tag
                    if t in action_dict:
                        curr_val = action_dict.get(t)
                        if curr_val == None:
                            action_list = [str(action)]
                            action_dict[t] = action_list
                        else:
                            curr_val.append(str(action))
                            action_dict[t] = curr_val
            elif node.find('method') != None:  # recover action
                if node.attrib.values():  # check if actions empty
                    t = int(list(node.attrib.values())[0].split("_")[2])
                    action = node.tag
                    if t in action_dict:
                        curr_val = action_dict.get(t)
                        if curr_val == None:
                            action_list = [str(action)]
                            action_dict[t] = action_list
                        else:
                            curr_val.append(str(action))
                            action_dict[t] = curr_val
        return action_dict

    def user_infected(self, file):
        infected_ids = []
        f = open(file)
        for line in f:
            l = line.strip().split(",")
            user_id = l[0]
            status = l[1]
            if status == "#FF0000":
                infected_ids.append(int(user_id))
        return infected_ids

    def get_id_from_username(self, username):
        if username == None:
            raise Exception("Username parameter blank")

        file = path_ + "/" + username + ".xml"

        parsed_xml = et.parse(file)
        # received  fromID_userID_time
        # sent  userID_toID_time
        # opened    userID_fromID_time
        # deleted   userID_fromID_time
        if parsed_xml.find("received") != None:
            id = parsed_xml.find("received").attrib['message_id']
            return self.split_id(id, 1)
        elif parsed_xml.find("sent") != None:
            id = parsed_xml.find("sent").attrib['message_id']
            return self.split_id(id, 0)
        elif parsed_xml.find("opened") != None:
            id = parsed_xml.find("opened").attrib['message_id']
            return self.split_id(id, 0)
        elif parsed_xml.find("deleted") != None:
            id = parsed_xml.find("deleted").attrib['message_id']
            return self.split_id(id, 0)

        return "Username not found"

    def get_username_from_id(self, user_id):
        if user_id == None:
            raise Exception("User ID parameter blank")

        all_files = glob.glob(path_ + "*.xml")
        for file in all_files:
            username = file.split("\\")[1].split(".")[0]
            uid = int(self.get_id_from_username(username))
            if uid == user_id:
                return username
        return "Username not found"

    def get_seeds(self):
        t0 = self.timestep_list()[0]

        parent_dir = pathlib.Path(path_).parent
        status_file = str(parent_dir) + '/status/' + str(t0) + '_status.csv'
        seed_ids = []

        f = open (status_file)
        for line in f:
            split_line = line.strip().split(",")
            if split_line[1] == "#FF0000":
                seed_ids.append(int(split_line[0]))

        return seed_ids




    def user_is_seed(self, user_id=None, username=None):
        '''
        Function takes either numerical user ID used in the tracking files, or username
        and checks if the user was infected during given round
        :param user_id: numerical user ID
        :param username: String username
        :return: boolean value
        '''
        seed_ids = self.get_seeds()

        if user_id != None:
            if user_id in seed_ids:
                return True
        elif username != None:
            user_id = self.get_id_from_username(username)
            if user_id in seed_ids:
                return True
        elif username == None and user_id == None:
            raise Exception("No parameters passed")
        return False

    def user_infected_in_round(self, user_id=None, username=None):
        '''
        Doesn't take into account if the user was seed, but will return a boolean value if user was infected in the given round
        :param user_id:
        :param username:
        :return: bolean
        '''
        infected_ids = self.list_of_infected()
        if user_id != None:
            if user_id in infected_ids:
                return True
        elif username != None:
            uid = self.get_id_from_username(username)
            if uid in infected_ids:
                return True
        elif user_id == None and username == None:
            raise Exception("No parameters passed")
        return False

    def list_of_infected(self):
        '''

        :return: list of all user_ids infected in the round
        '''
        parent_dir = pathlib.Path(path_).parent
        status_files =list(glob.iglob(str(parent_dir) + '/status/*_status.csv'))
        infected_ids = []

        for f in status_files:
            if f != "round.xml":
                infected_ids = infected_ids + self.user_infected(f)

        return list(set(infected_ids))

    def timestep_list(self):
        parent_dir = pathlib.Path(path_).parent
        status_files = list(glob.iglob(str(parent_dir) + '/status/*_status.csv'))
        t_list = []

        for file in status_files:
            f_name = ntpath.basename(file)
            timestep = f_name.split("_")[0]
            t_list.append(int(timestep))

        t_list.sort()

        return t_list


    def is_infected_from_status_list(self, f, status_list):
        f_name = ntpath.basename(f).strip().split(".")[0]
        user_id = str(self.get_id_from_username(f_name))
        for dicts in status_list:
            status = dicts.get(user_id)
            if status == "infected":
                return True
        return False

    def list_of_actions(self, user_id=None, username=None, timestep=None):
        '''
        If no parameters are passed, the function will return all actions at each timestep
        With user_id or username parameter, the function will return interactions from a specific user
        timestep parameter will get all the actions at a given timestep

        :param user_id: numerical user ID
        :param username: String username
        :param timestep: time t at which all actions occured
        :return: list of actions
        '''

        actions_dict = {}

        timestep_list = self.timestep_list()
        if user_id== None and username == None and timestep == None:
            actions_dict = dict.fromkeys(timestep_list, None) # each timestep will record all the actions that happened during it
            all_files = glob.glob(path_ + "*.xml")
            for f in all_files:
                if f != "round.xml":
                    actions_dict = self.update_action_dict(actions_dict, f)
        elif timestep!= None and (user_id != None or username!= None):
            if user_id != None:
                username = self.get_username_from_id(user_id)
            timestep_list = timestep_list[timestep]
            actions_dict = {timestep_list: None}
            f = path_ + username + ".xml"
            if f != "round.xml":
                actions_dict = self.update_action_dict(actions_dict, f)
        elif timestep != None:
            timestep_list = timestep_list[timestep] # get timestep at a given second
            actions_dict = {timestep_list: None}
            all_files = glob.glob(path_ + "*.xml")
            for f in all_files:
                if f != "round.xml":
                    actions_dict = self.update_action_dict(actions_dict, f)
        elif username != None:
            actions_dict = dict.fromkeys(timestep_list, None)
            f = path_ + username + ".xml"
            if f != "round.xml":
                actions_dict = self.update_action_dict(actions_dict, f)
        elif user_id != None:
            username = self.get_username_from_id(user_id)
            actions_dict = dict.fromkeys(timestep_list, None)
            f = path_ + username + ".xml"
            if f != "round.xml":
                actions_dict = self.update_action_dict(actions_dict, f)
        return actions_dict

    def get_actions(self, f, append_data, append_bool, neighbour_id=None):
        actions = []
        user_inf = False
        parsed_xml = et.parse(f)

        timesteps = self.timestep_list()
        timesteps.sort()

        nd = network_data()

        # Actions between all the neighbours
        if neighbour_id == None:
            for node in parsed_xml.getroot():
                # print(node)
                if node.find('blocked_user') == None and node.find('method') == None:
                    if node.find('user_infected') != None:
                        if node.find('user_infected').text != None:
                            time_t = int(dict(node.attrib).get("message_id").split("_")[2])
                            if time_t in timesteps:
                                time_index = timesteps.index(time_t)
                                user_inf = self.is_infected_from_status_list(f, nd.network_status_at_time(time_index))
                    if user_inf == True:
                        append_data = append_bool
                    if append_data:
                        actions.append(node.tag)
                elif node.find('blocked_user') != None:  # blocked action
                    actions.append(node.tag)
                elif node.find('method') != None:  # recover action
                    actions.append(node.tag)
        elif neighbour_id != None:
            for node in parsed_xml.getroot():
                node_tag = node.tag
                node_attributes = node.attrib
                if node_tag != None and node_attributes:
                    time_t = int(dict(node.attrib).get("message_id").split("_")[2])

                    if time_t in timesteps:
                        time_index = timesteps.index(time_t)
                        user_inf = self.is_infected_from_status_list(f, nd.network_status_at_time(time_index))

                    user_a = int(node_attributes.get("message_id").split("_")[0])
                    user_b = int(node_attributes.get("message_id").split("_")[1])
                    i_list = [user_a, user_b]

                    username = os.path.basename(f).strip().split(".")[0]

                    user_a_id = self.get_id_from_username(username)
                    user_b_id = neighbour_id
                    if user_a_id != None and user_b_id != None:
                        if user_a_id in i_list and user_b_id in i_list:
                            if user_inf == True:
                                append_data = append_bool
                            if append_data:
                                actions.append(node_tag)
        return actions

    def actions_before_infection(self, user_id=None, username=None, neighbour_id=None):
        '''
        :param user_id: numerical user ID
        :param username: String username
        :return: If no parameters passed, return actions before infection for all users, otherwise return for specific user
        '''

        append_data = True
        append_bool = False

        action_list = []

        if user_id == None and username== None:
            all_files = glob.glob(path_ + "*.xml")
            for f in all_files:
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool)
        elif (user_id != None or username != None) and neighbour_id != None:
            if user_id != None:
                f = path_ + "/" + self.get_username_from_id(user_id) + ".xml"
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool, neighbour_id=neighbour_id)
            else:
                f = path_ + "/" + username + ".xml"
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool, neighbour_id=neighbour_id)
        elif user_id != None:
            f = path_ + "/" + self.get_username_from_id(user_id) + ".xml"
            if f != "round.xml":
                action_list = action_list + self.get_actions(f, append_data, append_bool)
        elif username != None:
            f = path_ + "/" + username + ".xml"
            if f != "round.xml":
                action_list = action_list + self.get_actions(f, append_data, append_bool)

        return action_list

    def actions_after_infection(self, user_id=None, username=None, neighbour_id=None):
        '''
        :param user_id: numerical user ID
        :param username: String username
        :return: If no parameters passed, return actions after infection for all users, otherwise return for specific user
        '''

        append_data = False
        append_bool = True

        action_list = []

        if user_id == None and username == None:
            all_files = glob.glob(path_ + "*.xml")
            for f in all_files:
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool)
        elif (user_id != None or username != None) and neighbour_id != None:
            if user_id != None:
                f = path_ + "/" + self.get_username_from_id(user_id) + ".xml"
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool, neighbour_id=neighbour_id)
            else:
                f = path_ + "/" + username + ".xml"
                if f != "round.xml":
                    action_list = action_list + self.get_actions(f, append_data, append_bool, neighbour_id=neighbour_id)
        elif user_id != None:
            f = path_ + "/" + self.get_username_from_id(user_id) + ".xml"
            if f != "round.xml":
                action_list = action_list + self.get_actions(f, append_data, append_bool)
        elif username != None:
            f = path_ + "/" + username + ".xml"
            if f != "round.xml":
                action_list = action_list + self.get_actions(f, append_data, append_bool)
        return action_list

    def infection_dataframe(self, filename):
        '''
        convert the XML file into a pandas dataframe, with information about each timestep and infection of the given user/file at each time t
        :param filename:
        :return:
        '''
        dfcols = ['message_id', 'time', 'user_infected', 'message_infected']
        df = pd.DataFrame(columns=dfcols)

        f = path_ + filename

        if f != "round.xml":
            parsed_xml = ET.parse(f)
            for node in parsed_xml.getroot():
                message_id = node.attrib.get('message_id')
                t = node.find('time')
                user_inf = node.find('user_infected')
                message_inf = node.find('message_infected')

                df = df.append(
                    pd.Series([message_id, self.getvalueofnode(t), self.getvalueofnode(user_inf), self.getvalueofnode(message_inf)],
                              index=dfcols),
                    ignore_index=True)
            return df

    def interactions_between_nodes(self, user_id_a, user_id_b):

        timestep_list = self.timestep_list()
        node_a_actions = dict.fromkeys(timestep_list, None)
        node_b_actions = dict.fromkeys(timestep_list, None)

        username_a = self.get_username_from_id(user_id_a)
        f_a = path_ + username_a + ".xml"
        if f_a != "round.xml":
            node_a_actions = self.update_dict(node_a_actions, f_a, user_id_a, user_id_b)

        username_b = self.get_username_from_id(user_id_b)
        f_b = path_ + username_b + ".xml"
        if f_b != "round.xml":
            node_b_actions = self.update_dict(node_b_actions, f_b, user_id_a, user_id_b)

        return node_a_actions, node_b_actions

    def count_action(self, list_of_actions=None, action_type=None):
        '''
        The function takes in the list of actions from the interactions_between_nodes function and counts either all of the actions or a specific action type
        :param list_of_actions: the dict returned by interactions_between_nodes() function
        :param action_type: String value, if you want to count a specific action e.g. "opened_item"
        :return: a dict with counted values
        '''
        if list_of_actions == None:
            raise Exception("You must pass in the list of actions")
        if list_of_actions != None and action_type == None: # count all actions
            action_list = []
            for a in list_of_actions.values():
                if a != None:
                    action_list.extend(a)
            return Counter(action_list)
        elif list_of_actions != None and action_type != None:
            action_list = list_of_actions.values()
            act = 0
            for a in action_list:
                if a != None:
                    ac = Counter(a).get(action_type)
                    if ac != None:
                        act += ac

            return {action_type : act}

        return {}

    def interacted_in_scenario(self, user_id_a, user_id_b):
        '''
        Check if two users interacted with each other during the scenario
        :param user_id_a: source node numeric ID
        :param user_id_b: target node numeric ID
        :return: boolean, True if the two interacted, False if they didn't
        '''

        total_actions = []
        a_actions, b_actions = self.interactions_between_nodes(user_id_a, user_id_b)
        total_actions.extend(a_actions.values())
        total_actions.extend(b_actions.values())

        for a  in total_actions:
            if a != None:
                return True

        return False
