'''analyse clicks

Usage:
    analyse.py (--logfile=<input>)

Options:
    --logfile=<input>           npy-file
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
#from docopt import docopt

########################################################

# adjust your key assignment here, if different
key_assign = {
    'Out' :             'e',
    'Blue Goal' :       't',
    'Red Defense' :     '6',
    'Blue Forward' :    '5',
    'Red Midfield' :    '4',
    'Blue Midfield' :   '3',
    'Red Forward' :     '2',
    'Blue Defense' :    '1',
    'Red Goal' :        'q',
    'Game Break' :      '0',
    'Red Timeout' :     'w',
    'Blue Timeout' :    'r',
    }
###

ball = {
    'Out' :            0,
    'Blue Goal' :       1,
    'Red Defense' :     2,
    'Blue Forward' :    3,
    'Red Midfield' :    4,
    'Blue Midfield' :   5,
    'Red Forward' :     6,
    'Blue Defense' :    7,
    'Red Goal' :        8,
    'Game Break' :      9,
    'Red Timeout' :     4.5,
    'Blue Timeout' :    4.5
    }


team = ('Defense', 'Midfield', 'Forward')
team_color = ('g', 'b', 'r')
teams = ('Blue', 'Red')
teams_color = ('b', 'r')

team_red = np.array(['Red Defense', 'Red Midfield', 'Red Forward'])
team_blu = np.array(['Blue Defense', 'Blue Midfield', 'Blue Forward'])
rod_def = ('Blue Defense',  'Red Defense'  )
rod_5er = ('Blue Midfield', 'Red Midfield' )
rod_3er = ('Blue Forward',  'Red Forward'  )


##########################################################################3
##########################################################################3

game_name = input("Enter game name [Date, Teams, Game]:\n")
game_raw = input("Enter game data:\n")

data = np.array(list(game_raw))


# read data and 'constructor'
def proc_data(data):
    # data
    #print("Loading log file:", file_name)
    #data = np.loadtxt(file_name, delimiter=';', skiprows=0, dtype={
    #   'names': ('times', 'clicks'),
    #  'formats': ('float64', 'S9')})
    # start, end
    # first Midfield posession
    start = np.where((data == key_assign['Red Midfield']) |
            (data == key_assign['Blue Midfield']) |
            (data == key_assign['Game Break'])
            )[0][0]
    # until Control L = exit program
    #end = np.where((data['clicks'] == 'Control_L'))[0][-1]
    # until last goal
    end = np.where((data == key_assign['Red Goal']) |
            (data == key_assign['Blue Goal'])
            )[0][-1] + 3 # to have the score
    clicks = data[start:end]
    # time proc.
    #time_pos = times - times[0]
    #time_diff = times[1:] - times[:-1]
    # data proc.
    ball_pos = np.zeros(len(clicks))
    # here happens the key-ball assignment
    for name, value in key_assign.items():
        ball_pos[np.where(clicks == value)[0]] = ball[name]
    # clean zeroes for plotting
    index = np.where(ball_pos == 0.0)[0]
    ball_pos[index] = 4.5 # ball_pos[index-1]

    #print(ball_pos, clicks)
    #print(len(time_pos), len(ball_pos), len(clicks), len(time_diff))
    #print(clicks[ball_pos == 0.0]) # should be only numbers from goals and sets and timeouts
    return ball_pos, clicks

ball_pos, clicks = proc_data(data)


##########################################################################3
# rod&goal&timeout posession
def posession(ball_pos, position):
    rod_posessions = np.where(ball_pos == ball[position])[0]
    # counts, total_time, average
    return {'total': len(ball_pos),  # 
            'counts': len(rod_posessions), # 
            'fraction': len(rod_posessions)/len(ball_pos)} # 

#print(posession(ball_pos, 'Blue Forward'))
#print(posession(ball_pos, 3))




##########################################################################3

def from_to(ball_pos, rod_start, rod_end):
    index = np.where(ball_pos==ball[rod_start])[0]
    #print(index + 1:w)
    successes = len(np.where(ball_pos[index+1] == ball[rod_end])[0])
    return successes
	
	
#print(from_to(ball_pos, 'Blue Midfield', 'Blue Forward'))

##########################################################################3

def from_to_statistics(ball_pos, from_position):
    if from_position[:3] == 'Red':
        off_2er =  'Red Defense'
        off_5er =  'Red Midfield'
        off_3er =  'Red Forward'
        off_goal = 'Red Goal'
        def_2er =  'Blue Defense'
        def_5er =  'Blue Midfield'
        def_3er =  'Blue Forward'
        def_goal = 'Blue Goal'
    elif from_position[:4] == 'Blue':
        off_2er =  'Blue Defense'
        off_5er =  'Blue Midfield'
        off_3er =  'Blue Forward'
        off_goal = 'Blue Goal'
        def_2er =  'Red Defense'
        def_5er =  'Red Midfield'
        def_3er =  'Red Forward'
        def_goal = 'Red Goal'
    else:
        exit()
    # total ball posession
    total = posession(ball_pos, from_position)['total']
    # positive offense play
    pass2er = from_to(ball_pos, from_position, off_2er)
    pass5er = from_to(ball_pos, from_position, off_5er)
    pass3er = from_to(ball_pos, from_position, off_3er)
    goals = from_to(ball_pos, from_position, off_goal)
    total_off = pass2er + pass5er + pass3er + goals
    # positive offense play
    turnover_2er = from_to(ball_pos, from_position, def_2er)
    turnover_5er = from_to(ball_pos, from_position, def_5er)
    turnover_3er = from_to(ball_pos, from_position, def_3er)
    own_goals = from_to(ball_pos, from_position, def_goal)
    total_def = turnover_2er + turnover_5er + turnover_3er + own_goals
    #print(team, active_rod, '(', rod, ') = ', total)
    #print(total_off, '=', pass2er, pass5er, pass3er, goals)
    #print(total_def, '=', turnover_2er, turnover_5er, turnover_3er, own_goals)
    return (own_goals, turnover_3er, turnover_5er, turnover_2er,
            pass2er, pass5er, pass3er, goals)
			
			
#print(from_to_statistics(ball_pos, 'Blue Midfield'))

##########################################################################3


# timeline
def plot_timeline(ball_pos, game):
    time_pos = np.arange(len(ball_pos))

    # plot
    fig, ax = plt.subplots(figsize=(6, 2))#, dpi=100)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.2)

    # table
    ax.axhspan(ymin=1.0, ymax=1.5, alpha=0.75, color='b', lw=0)
    ax.axhspan(ymin=1.5, ymax=2.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=2.5, ymax=3.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=3.5, ymax=4.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=4.5, ymax=5.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=5.5, ymax=6.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=6.5, ymax=7.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=7.5, ymax=8.0, alpha=0.75, color='r', lw=0)

    # ball position
    #plt.plot(time_norm, ball_pos)
    plt.plot(time_pos, ball_pos, color='k', lw=1)

    # goals
    goals_index = np.where(ball_pos == ball['Red Goal'])[0]
    for index in range(len(goals_index)):
        ax.axvspan(xmin=time_pos[goals_index][index], xmax=time_pos[goals_index][index]+1,
                #alpha=0.75, 
                color='r', lw=0)
    goals_index = np.where(ball_pos == ball['Blue Goal'])[0]
    for index in range(len(goals_index)):
        ax.axvspan(xmin=time_pos[goals_index][index], xmax=time_pos[goals_index][index]+1,
                #alpha=0.75, 
                color='b', lw=0)

    # x-axis: time 
    ax.set_xlabel('action')
    ax.set_xlim(xmin=0.0)

    # y-axis: ball location 
    #ax.set_ylabel('position')
    ax.set_ylim(1., 8.)
    # change to names
    ax.locator_params(nbins=8, axis='y')
    #ax.yaxis.set_ticks(np.arange(0, 8, 9))
    y_tick_labels = ax.get_yticks().tolist()
    #print y_tick_labels
    y_tick_labels[0] = 'Tor'
    y_tick_labels[1] = 'Abw.' # red
    y_tick_labels[2] = '3er'  # blue
    y_tick_labels[3] = '5er'  # red
    y_tick_labels[4] = '5er'  # blue
    y_tick_labels[5] = '3er'  # red
    y_tick_labels[6] = 'Abw.' # blue
    y_tick_labels[7] = 'Tor'
    ax.set_yticklabels(y_tick_labels)

    # save
    save_name = 'out/' + game + '_ball_positions' + '.png'
    fig.savefig(save_name)

plot_timeline(ball_pos, game_name)


# goals
def plot_goals(ball_pos, game):
    # plot
    fig, ax = plt.subplots(figsize=(4, 3))#, dpi=100)
    fig.subplots_adjust(left=0.15, right=0.98, top=0.97, bottom=0.15)

    goal_index = np.where(ball_pos == ball['Red Goal'])[0]
    #print(goal_index)
    actions = np.arange(len(ball_pos))
    time = np.append(actions[0], actions[goal_index])
    goals = np.arange(len(actions[goal_index])+1)
    plt.plot(time, goals, 'r', marker='o')

    goal_index = np.where(ball_pos == ball['Blue Goal'])[0]
    #print(goal_index)
    actions = np.arange(len(ball_pos))
    time = np.append(actions[0], actions[goal_index])
    goals = np.arange(len(actions[goal_index])+1)
    plt.plot(time, goals, 'b', marker='o')

    ax.set_xlabel('actions #')
    ax.set_ylabel('goals #')
    spacing = 1
    minorLocator = MultipleLocator(spacing)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.grid(which = 'minor')

    # save
    save_name = 'out/' + game + '_goals' + '.png'
    fig.savefig(save_name)

plot_goals(ball_pos, game_name)


# stackd histo
def plot_bar(values, labels, colors, xpos, width, legend, ax):
    bottom = 0
    for index, value in enumerate(values):
        plt.bar(xpos, value, width, bottom=bottom,
                label=labels[index], color=colors[index])
        bottom += value
        if legend == True:
            if value != 0:
                ax.text(xpos, bottom - 0.5, labels[index],
                        horizontalalignment='center', verticalalignment='center')

# event statistic
def plot_success(ball_pos, game):
    # from to statistics
    # plot
    fig, ax = plt.subplots(figsize=(9, 6))#, dpi=100)
    fig.subplots_adjust(left=0.05, right=0.98, top=0.97, bottom=0.15)

    for position, index in ball.items(): # note: not ordered dict iter
        #print position, index
        if position == 'Blue Goal' or position == 'Red Goal':
            fracs = posession(ball_pos, position)['counts']
            labels = str(fracs)
            # Blue Goal
            if position == 'Blue Goal':
                colors = 'b'
            elif position == 'Red Goal':
                colors = 'r'
            plot_bar([fracs], [labels], colors, xpos=index, width=0.65, legend=True, ax=ax)
        if position == 'Red Defense' or position == 'Blue Defense':
            labels =  ('own goal', 'turnover 3er', 'turnover 5er', 'turnover_2er',
                     'retry', 'pass 5er', 'pass 3er', 'goal')
            colors=('r', 'tab:orange', 'y', 'y',
                    '0.5', '0.7', 'b', 'g')
            if position == 'Red Defense':
                fracs  = from_to_statistics(ball_pos, 'Red Defense')

            elif position == 'Blue Defense':
                fracs  = from_to_statistics(ball_pos, 'Blue Defense')

            plot_bar(fracs, labels, colors, xpos=index, width=0.65, legend=True, ax=ax)

        if position == 'Red Midfield' or position == 'Blue Midfield':
            labels =  ('own goal', 'turnover 3er', 'turnover 5er', 'turnover_2er',
                     'loose to 2er', 'retry', 'pass 3er', 'goal')
            colors=('r', 'tab:orange', 'y', 'y',
                    '0.5', 'b', 'b', 'g')
            if position == 'Red Midfield':
                fracs  = from_to_statistics(ball_pos, 'Red Midfield')
            elif position == 'Blue Midfield':
                fracs  = from_to_statistics(ball_pos, 'Blue Midfield')
            plot_bar(fracs, labels, colors, xpos=index, width=0.65, legend=True, ax=ax)

        if position == 'Red Forward' or position == 'Blue Forward':
            labels =  ('own goal', 'turnover 3er', 'turnover 5er', 'turnover_2er',
                     'loose to 2 er', 'loose to 5er', 'retry', 'goal')
            colors=('r', 'tab:orange', 'y', 'y',
                    '0.5', '0.7', 'b', 'g')
            if position == 'Red Forward':
                fracs  = from_to_statistics(ball_pos, 'Red Forward')

            elif position == 'Blue Forward':
                fracs  = from_to_statistics(ball_pos, 'Blue Forward')

            plot_bar(fracs, labels, colors, xpos=index, width=0.65, legend=True, ax=ax)

    # x labels
    tick_names = list(ball.keys())
    #print tick_names
    x_positions = [ball[name] for name in tick_names]
    plt.xticks(x_positions, tick_names, rotation='45')
    # options
    plt.xlim(0.5, 8.5)
    # grid lines
    spacing = 1
    minorLocator = MultipleLocator(spacing)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.grid(which = 'minor')

    # TODO: opt. team colors

    # save
    save_name = 'out/' + game + '_success' + '.png'
    fig.savefig(save_name)
	

plot_success(ball_pos, game_name)


####################
# std printout 
print("\n")

red_turnover_total = 0
red_retry_total = 0
red_offense_total = 0
red_goals_total = 0

red_turnover_total_rel = 0.
red_retry_total_rel = 0.
red_offense_total_rel = 0.

blue_turnover_total = 0
blue_retry_total = 0
blue_offense_total = 0
blue_goals_total = 0

blue_turnover_total_rel = 0.
blue_retry_total_rel = 0.
blue_offense_total_rel = 0.

####################################################################
# from_to_statistics
# output: own_goals, turnover_3er, turnover_5er, turnover_2er, pass2er, pass5er, pass3er, goals
# list from 0 till 7

red_fracs = from_to_statistics(ball_pos, 'Red Defense')
#print(red_fracs)
red_turnover = np.sum(red_fracs[:4])
red_retry    = np.sum(red_fracs[4])
red_offense  = np.sum(red_fracs[5:])
red_goals    = red_fracs[7]
red_turnover_rel = round(red_turnover/np.sum(red_fracs)*100., 1)
red_retry_rel    = round(red_retry/np.sum(red_fracs)*100., 1)
red_offense_rel  = round(red_offense/np.sum(red_fracs)*100. , 1)

blue_fracs = from_to_statistics(ball_pos, 'Blue Defense')
#print(blue_fracs)
blue_turnover = np.sum(blue_fracs[:4])
blue_retry    = np.sum(blue_fracs[4])
blue_offense  = np.sum(blue_fracs[5:])
blue_goals    = blue_fracs[7]
blue_turnover_rel = round(blue_turnover/np.sum(blue_fracs)*100., 1)
blue_retry_rel    = round(blue_retry/np.sum(blue_fracs)*100., 1)
blue_offense_rel  = round(blue_offense/np.sum(blue_fracs)*100. , 1)

print("           Red Defense     Blue Defense", "\n" 
      " Goals:   ", red_goals, " (-", red_fracs[0], ")      ", blue_goals, " (-", blue_fracs[0], ")", "\n", 
      "Offense: ", red_offense_rel,  "% (", red_offense, ")   ", blue_offense_rel,  "% (", blue_offense,")",  "\n",
      "Retry:   ", red_retry_rel,    "% (", red_retry,   ")   ", blue_retry_rel,    "% (", blue_retry,    ")", "\n",
      "Turnover:", red_turnover_rel, "% (", red_turnover,")   ",blue_turnover_rel, "% (", blue_turnover,")", "\n")

red_turnover_total = red_turnover_total + red_turnover 
red_retry_total    = red_retry_total    + red_retry
red_offense_total  = red_offense_total  + red_offense
red_goals_total    = red_goals_total    + red_goals     + blue_fracs[0]

red_turnover_total_rel = red_turnover_total_rel + red_turnover_rel
red_retry_total_rel    = red_retry_total_rel    + red_retry_rel
red_offense_total_rel  = red_offense_total_rel  + red_offense_rel

blue_turnover_total = blue_turnover_total + blue_turnover
blue_retry_total    = blue_retry_total    + blue_retry
blue_offense_total  = blue_offense_total  + blue_offense
blue_goals_total    = blue_goals_total    + blue_goals    + red_fracs[0]

blue_turnover_total_rel = blue_turnover_total_rel + blue_turnover_rel
blue_retry_total_rel    = blue_retry_total_rel    + blue_retry_rel
blue_offense_total_rel  = blue_offense_total_rel  + blue_offense_rel


####################################################################
# from_to_statistics
# output: own_goals, turnover_3er, turnover_5er, turnover_2er, pass2er, pass5er, pass3er, goals
# list from 0 till 7

red_fracs = from_to_statistics(ball_pos, 'Red Midfield')
#print(red_fracs)
red_turnover = np.sum(red_fracs[:4])
red_retry    = np.sum(red_fracs[4:6])
red_offense  = np.sum(red_fracs[6:])
red_goals    = red_fracs[7]
red_turnover_rel = round(red_turnover/np.sum(red_fracs)*100., 1)
red_retry_rel    = round(red_retry/np.sum(red_fracs)*100., 1)
red_offense_rel  = round(red_offense/np.sum(red_fracs)*100. , 1)

blue_fracs = from_to_statistics(ball_pos, 'Blue Midfield')
#print(blue_fracs)
blue_turnover = np.sum(blue_fracs[:4])
blue_retry    = np.sum(blue_fracs[4:6])
blue_offense  = np.sum(blue_fracs[6:])
blue_goals    = blue_fracs[7]
blue_turnover_rel = round(blue_turnover/np.sum(blue_fracs)*100., 1)
blue_retry_rel    = round(blue_retry/np.sum(blue_fracs)*100., 1)
blue_offense_rel  = round(blue_offense/np.sum(blue_fracs)*100. , 1)

print("           Red Midfield    Blue Midfield", "\n" 
      " Goals:   ", red_goals, " (-", red_fracs[0], ")      ", blue_goals, " (-", blue_fracs[0], ")", "\n", 
      "Offense: ", red_offense_rel,  "% (", red_offense, ")   ", blue_offense_rel,  "% (", blue_offense,")",  "\n",
      "Retry:   ", red_retry_rel,    "% (", red_retry,   ")   ", blue_retry_rel,    "% (", blue_retry,    ")", "\n",
      "Turnover:", red_turnover_rel, "% (", red_turnover,")   ", blue_turnover_rel, "% (", blue_turnover,")", "\n")

red_turnover_total = red_turnover_total + red_turnover 
red_retry_total    = red_retry_total    + red_retry
red_offense_total  = red_offense_total  + red_offense
red_goals_total    = red_goals_total    + red_goals     + blue_fracs[0]

red_turnover_total_rel = red_turnover_total_rel + red_turnover_rel
red_retry_total_rel    = red_retry_total_rel    + red_retry_rel
red_offense_total_rel  = red_offense_total_rel  + red_offense_rel

blue_turnover_total = blue_turnover_total + blue_turnover
blue_retry_total    = blue_retry_total    + blue_retry
blue_offense_total  = blue_offense_total  + blue_offense
blue_goals_total    = blue_goals_total    + blue_goals    + red_fracs[0]

blue_turnover_total_rel = blue_turnover_total_rel + blue_turnover_rel
blue_retry_total_rel    = blue_retry_total_rel    + blue_retry_rel
blue_offense_total_rel  = blue_offense_total_rel  + blue_offense_rel

####################################################################
# from_to_statistics
# output: own_goals, turnover_3er, turnover_5er, turnover_2er, pass2er, pass5er, pass3er, goals
# list from 0 till 7

red_fracs = from_to_statistics(ball_pos, 'Red Forward')
#print(red_fracs)
red_turnover = np.sum(red_fracs[:4])
red_retry    = np.sum(red_fracs[4:7])
red_offense  = np.sum(red_fracs[7])
red_goals    = red_fracs[7]
red_turnover_rel = round(red_turnover/np.sum(red_fracs)*100., 1)
red_retry_rel    = round(red_retry/np.sum(red_fracs)*100., 1)
red_offense_rel  = round(red_offense/np.sum(red_fracs)*100. , 1)

blue_fracs = from_to_statistics(ball_pos, 'Blue Forward')
#print(blue_fracs)
blue_turnover = np.sum(blue_fracs[:4])
blue_retry    = np.sum(blue_fracs[4:7])
blue_offense  = np.sum(blue_fracs[7])
blue_goals    = blue_fracs[7]
blue_turnover_rel = round(blue_turnover/np.sum(blue_fracs)*100., 1)
blue_retry_rel    = round(blue_retry/np.sum(blue_fracs)*100., 1)
blue_offense_rel  = round(blue_offense/np.sum(blue_fracs)*100. , 1)

print("           Red Forward     Blue Forward", "\n" 
      " Goals:   ", red_goals, " (-", red_fracs[0], ")      ", blue_goals, " (-", blue_fracs[0], ")", "\n", 
      "Offense: ", red_offense_rel,  "% (", red_offense, ")   ", blue_offense_rel,  "% (", blue_offense,  ")", "\n",
      "Retry:   ", red_retry_rel,    "% (", red_retry,   ")   ", blue_retry_rel,    "% (", blue_retry,    ")", "\n",
      "Turnover:", red_turnover_rel, "% (", red_turnover,")   ", blue_turnover_rel, "% (", blue_turnover, ")", "\n")

red_turnover_total = red_turnover_total + red_turnover 
red_retry_total    = red_retry_total    + red_retry
red_offense_total  = red_offense_total  + red_offense
red_goals_total    = red_goals_total    + red_goals     + blue_fracs[0]

red_turnover_total_rel = round((red_turnover_total_rel + red_turnover_rel)/3, 1)
red_retry_total_rel    = round((red_retry_total_rel    + red_retry_rel)/3, 1)
red_offense_total_rel  = round((red_offense_total_rel  + red_offense_rel)/3, 1)

blue_turnover_total = blue_turnover_total + blue_turnover
blue_retry_total    = blue_retry_total    + blue_retry
blue_offense_total  = blue_offense_total  + blue_offense
blue_goals_total    = blue_goals_total    + blue_goals    + red_fracs[0]

blue_turnover_total_rel = round((blue_turnover_total_rel + blue_turnover_rel)/3, 1)
blue_retry_total_rel    = round((blue_retry_total_rel    + blue_retry_rel)/3, 1)
blue_offense_total_rel  = round((blue_offense_total_rel  + blue_offense_rel)/3, 1)


print("           Red Total       Blue Total", "\n" 
      " Goals:   ", red_goals_total, "             ", blue_goals_total, "\n", 
      "Offense: ", red_offense_total_rel,  "% (", red_offense_total, ")   ", blue_offense_total_rel,  "% (", blue_offense_total,  ")", "\n",
      "Retry:   ", red_retry_total_rel,    "% (", red_retry_total,   ")   ", blue_retry_total_rel,    "% (", blue_retry_total,    ")", "\n",
      "Turnover:", red_turnover_total_rel, "% (", red_turnover_total,")   ", blue_turnover_total_rel, "% (", blue_turnover_total, ")", "\n")


################
# save total
print("\n")

import os.path
fname = 'out/total.npz'

if os.path.isfile(fname):
    print("Add up")
    data = np.load(fname)
    red = data['red'] + np.array([red_turnover_total, red_retry_total, red_offense_total, red_goals_total])
    red_rel = data['red_rel']/2 + np.array([red_turnover_total_rel, red_retry_total_rel, red_offense_total_rel])/2  
    blue = data['blue'] + np.array([blue_turnover_total, blue_retry_total, blue_offense_total, blue_goals_total])   
    blue_rel = data['blue_rel']/2 + np.array([blue_turnover_total_rel, blue_retry_total_rel, blue_offense_total_rel])/2
    data.close()
else:
    print("New")
    red = np.array([red_turnover_total, red_retry_total, red_offense_total, red_goals_total])
    red_rel = np.array([red_turnover_total_rel, red_retry_total_rel, red_offense_total_rel])
    blue = np.array([blue_turnover_total, blue_retry_total, blue_offense_total, blue_goals_total])   
    blue_rel = np.array([blue_turnover_total_rel, blue_retry_total_rel, blue_offense_total_rel])

np.savez(fname, red=red, red_rel=red_rel, blue=blue, blue_rel=blue_rel)

print("           Red Sum          Blue Sum", "\n" 
      " Goals:   ", red[3], "             ", blue[3], "\n", 
      "Offense: ", red_rel[2],  "% (", red[2], ")   ", blue_rel[2],  "% (", blue[2],  ")", "\n",
      "Retry:   ", red_rel[1],    "% (", red[1],   ")   ", blue_rel[1],    "% (", blue[1],    ")", "\n",
      "Turnover:", red_rel[0], "% (", red[0],")   ", blue_rel[0], "% (", blue[0], ")", "\n")
