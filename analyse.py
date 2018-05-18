'''analyse clicks

Usage:
    analyse.py (--input=<input>)

Options:
    --input=<input>             npy-file
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from docopt import docopt

#import histmath as hm

#                     Null, Tor, Abw, 3er, 5er, 5er, 3er, Abw, Tor 
key_assign = np.array(['0', 'r', 'd', 'f', 'g', 'h', 'j', 'k', 'u'])
# code assign   array(['0', '1', '2', '3', '4', '5', '6', '7', '8'])
team = ('Defense', 'Midfield', 'Forward')
team_rod = np.array(['Defense', 'Midfield', 'Forward'])
team_color = ('g', 'b', 'r')
teams = ('Red', 'Blue')
teams_color = ('r', 'b')
team_red = np.array([2, 4, 6])
team_blu = np.array([7, 5, 3])
rod_def = (2, 7)
rod_5er = (4, 5)
rod_3er = (6, 3)
goal = (8, 1)



##########################################################################3
# read data and 'constructor'
def proc_data(file_name):
    # data
    arguments = docopt(__doc__, version='analyze trigger')
    file_name = arguments['--input']
    print "Loading log file:", file_name
    data = np.loadtxt(file_name, delimiter=';', skiprows=0, dtype={
        'names': ('times', 'clicks'),
        'formats': ('float64', 'S9')})
    # time proc.
    time_pos = data['times'] - data['times'][0]
    time_diff = data['times'][1:] - data['times'][:-1]
    # data proc.
    # for plot
    ball_pos = np.zeros(len(data['clicks']))
    for index, value in enumerate(key_assign):
        ball_pos[np.where(data['clicks']==key_assign[index])[0]] = index
    ball_pos[np.where(ball_pos==0.0)[0]] = 4.5

    return time_pos, ball_pos, data['clicks'], time_diff

##########################################################################3
def plot_timeline(time_pos, ball_pos):
    # for plot v2
    ball_pos2 = np.zeros(2*len(time_pos))
    time_pos2 = np.zeros(2*len(time_pos))
    # boxplot
    time_pos2[0::2] = time_pos
    time_pos2[1::2] = time_pos
    #print time_pos2
    ball_pos2[0::2] = ball_pos
    ball_pos2[1::2] = ball_pos
    #print ball_pos2

    # plot
    fig, ax = plt.subplots(figsize=(6, 2))#, dpi=100)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.2)

    # spielfeld
    ax.axhspan(ymin=1.0, ymax=1.5, alpha=0.75, color='b', lw=0)
    ax.axhspan(ymin=1.5, ymax=2.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=2.5, ymax=3.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=3.5, ymax=4.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=4.5, ymax=5.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=5.5, ymax=6.5, alpha=0.5, color='r', lw=0)
    ax.axhspan(ymin=6.5, ymax=7.5, alpha=0.5, color='b', lw=0)
    ax.axhspan(ymin=7.5, ymax=8.0, alpha=0.75, color='r', lw=0)

    # Ballverlauf
    #plt.plot(time_norm, ball_pos)
    plt.plot(time_pos2[1:], ball_pos2[0:-1], color='k', lw=1)

    # TODO:
    # Tore
    #ax.text(0.05, 0.9, timeline_text,
    #        transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
    # Aus

    # Timeout

    # x-axis: time 
    ax.set_xlabel('time in s')
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
    save_name = 'out/' + file_name[4:-4] + '_ball_positionen' + '.pdf'
    fig.savefig(save_name)
    print "evince", save_name, "&"

##########################################################################3
def goals(ball_pos, team):
    print ball_pos


##########################################################################3
def posession(time_pos, ball_pos, time_diff, rod):
    rod_posessions = time_diff[np.where(ball_pos==rod)[0]]
    # counts, total_time, average
    return {'counts': len(rod_posessions),  # absolut
            'time': np.sum(rod_posessions), # seconds
            'average': np.sum(rod_posessions)/len(rod_posessions)} # seconds

##########################################################################3
def plot_posession(time_pos, ball_pos, time_diff):
    # times
    red_abw = posession(time_pos, ball_pos, time_diff, 2)
    blu_3er = posession(time_pos, ball_pos, time_diff, 3)
    red_5er = posession(time_pos, ball_pos, time_diff, 4)
    blu_5er = posession(time_pos, ball_pos, time_diff, 5)
    red_3er = posession(time_pos, ball_pos, time_diff, 6)
    blu_abw = posession(time_pos, ball_pos, time_diff, 7)
    # total
    total_counts = 1.* red_abw['counts'] + blu_3er['counts'] + red_5er['counts'] + blu_5er['counts'] + red_3er['counts'] + blu_abw['counts']
    total_time = 1.* red_abw['time'] + blu_3er['time'] + red_5er['time'] + blu_5er['time'] + red_3er['time'] + blu_abw['time']
    total = {'counts': total_counts, 'time': total_time}

    if False:
        print "total", total['counts'], "#",  total['time'], "sec"
        print "red_abw:", red_abw
        print "red_abw:", 1.*red_abw['counts']/total['counts'], "%", red_abw['time']/total['time'], "%"
        print "blu_3er:", blu_3er
        print "blu_3er:", 1.*blu_3er['counts']/total['counts'], "%", blu_3er['time']/total['time'], "%"
        print "red_5er:", red_5er
        print "red_5er:", 1.*red_5er['counts']/total['counts'], "%", red_5er['time']/total['time'], "%"
        print "blu_5er:", blu_5er
        print "blu_5er:", 1.*blu_5er['counts']/total['counts'], "%", blu_5er['time']/total['time'], "%"
        print "red_3er:", red_3er
        print "red_3er:", 1.*red_3er['counts']/total['counts'], "%", red_3er['time']/total['time'], "%"
        print "blu_abw:", blu_abw
        print "blu_abw:", 1.*blu_abw['counts']/total['counts'], "%", blu_abw['time']/total['time'], "%"

    # stacked histo
    # rod_cfg: counts, time, average 
    def plot_bar(rod_cfg, parameter, xpos, width, legend, option):
        bottom = 0
        for index, value in enumerate(rod_cfg):
            rod = posession(time_pos, ball_pos, time_diff, value)
            if option == 'team':
                plt.bar(xpos, rod[parameter], width, bottom=bottom,
                        label=team[index], color=team_color[index])
            elif option == 'rod':
                plt.bar(xpos, rod[parameter], width, bottom=bottom,
                        label=teams[index], color=teams_color[index])
            bottom += rod[parameter]
        if legend == True:
            #plt.legend()
            #ax.legend(            
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[::-1], labels[::-1],
                loc='upper center', bbox_to_anchor=(0.5, 1.4),
                ncol=1, fancybox=True)#, shadow=True))#, title='Line', loc='upper left')

    # TODO: texts with number
    # teams: counts, time, average 
    for index, value in enumerate(('counts', 'time', 'average')):
        # plot
        fig, ax = plt.subplots(figsize=(2, 3))#, dpi=100)
        fig.subplots_adjust(left=0.3, right=0.98, top=0.75, bottom=0.1)

        plot_bar(team_red, value, xpos=1.0, width=0.65, legend=True,  option='team')
        plot_bar(team_blu, value, xpos=2.0, width=0.65, legend=False, option='team')

        # x-axis: time 
        ax.set_ylabel(value)
        #ax.set_xlim(xmin=0.0)

        # y-axis: ball location 
        #ax.set_ylabel('position')
        ax.set_xlim(0.6, 2.4)
        # change to names
        #ax.locator_params(nbins=2, axis='x')
        #ax.xaxis.set_ticks(np.arange(0.9, 2.1, 2))
        x_tick_labels = ax.get_xticks().tolist()
        #print x_tick_labels
        #print tick_labels
        x_tick_labels[1] = 'Red'
        x_tick_labels[2] = 'Blue'
        ax.set_xticklabels(x_tick_labels)

        # save
        save_name = 'out/' + file_name[4:-4] + '_ball_team_' + value + '.pdf'
        fig.savefig(save_name)
        print "evince", save_name, "&"

    # rods: counts, time, average 
    for index, value in enumerate(('counts', 'time', 'average')):
        # plot
        fig, ax = plt.subplots(figsize=(2, 3))#, dpi=100)
        fig.subplots_adjust(left=0.3, right=0.98, top=0.75, bottom=0.1)

        plot_bar(rod_def, value, xpos=1.0, width=0.65, legend=True,  option='rod')
        plot_bar(rod_5er, value, xpos=2.0, width=0.65, legend=False, option='rod')
        plot_bar(rod_3er, value, xpos=3.0, width=0.65, legend=False, option='rod')

        # x-axis: time 
        ax.set_ylabel(value)
        #ax.set_xlim(xmin=0.0)

        # y-axis: ball location 
        #ax.set_ylabel('position')
        ax.set_xlim(0.6, 3.4)
        # change to names
        #ax.locator_params(nbins=2, axis='x')
        #ax.xaxis.set_ticks(np.arange(0.9, 2.1, 2))
        x_tick_labels = ax.get_xticks().tolist()
        #print x_tick_labels
        #print tick_labels
        x_tick_labels[1] = 'Def.'
        x_tick_labels[2] = '5rod'
        x_tick_labels[3] = '3rod'
        ax.set_xticklabels(x_tick_labels)

        # save
        save_name = 'out/' + file_name[4:-4] + '_ball_rods_' + value + '.pdf'
        fig.savefig(save_name)
        print "evince", save_name, "&"

##########################################################################3
def success(ball_pos, rod_start, rod_end):
    #print ball_pos
    index = np.where(ball_pos==rod_start)[0]
    total = len(ball_pos[index])
    successes = len(np.where(ball_pos[index+1] == rod_end)[0])
    retries = len(np.where(ball_pos[index+1] == rod_start)[0])
    return {'successes': successes, 'retries': retries, 'total': total, 'rate': 1.*successes/total}

def from_to(ball_pos, rod_start, rod_end):
    index = np.where(ball_pos==rod_start)[0]
    successes = len(np.where(ball_pos[index+1] == rod_end)[0])
    return successes

# stacked histo
def plot_bar2(values, labels, colors, xpos, width, legend, ax):
    bottom = 0
    for index, value in enumerate(values):
        plt.bar(xpos, value, width, bottom=bottom,
                label=labels[index], color=colors[index])
        bottom += value
        if legend == True:
            if value != 0:
                ax.text(xpos, bottom - 0.5, labels[index],
                        horizontalalignment='center', verticalalignment='center')
        #plt.legend()
        #ax.legend(            
        #handles, labels = ax.get_legend_handles_labels()
        #ax.legend(handles[::-1], labels[::-1],
        #    loc='upper center', bbox_to_anchor=(0.5, 1.4),
        #    ncol=1, fancybox=True)#, shadow=True))#, title='Line', loc='upper left')

##########################################################################3
def plot_success(ball_pos, ball_pos_raw):
    # TODO: plot or table 
    # shoot statistics
    #print "red 3er", success(ball_pos, 6, 8)
    #print "red 3er, raw", success(ball_pos_raw, 'j', 'u')
    #print "red 5er", success(ball_pos, 4, 6)
    #print "def red", success(ball_pos, 6, 7)


    def plot_success_pie(rod_start, rod_end):
        rod = success(ball_pos, rod_start, rod_end)
        print "result", rod
        successes = 100.*rod['successes']/rod['total']
        retries = 100.*rod['retries']/rod['total']
        fails = 100.*(rod['total']-rod['successes']-rod['retries'])/rod['total']
        fracs  = (successes, retries, fails)
        print fracs
        labels = (rod['successes'], rod['retries'], rod['total']-rod['successes']-rod['retries'])
        plt.pie(fracs, labels=labels, shadow=True, colors=('g', 'b', 'r'))
    
    def plot_catch_pie(rod_start, rod_end):
        # block 3-3, catch 3-2, goals 3-1
        rod = success(ball_pos, rod_start, rod_end)
        print "result", rod
        successes = 100.*rod['successes']/rod['total']
        retries = 100.*rod['retries']/rod['total']
        fails = 100.*(rod['total']-rod['successes']-rod['retries'])/rod['total']
        fracs  = (successes, retries, fails)
        print fracs
        labels = (rod['successes'], rod['retries'], rod['total']-rod['successes']-rod['retries'])
        plt.pie(fracs, labels=labels, shadow=True, colors=('g', 'b', 'r'))
    
    def plot_defense_pie(team):
        print team
        if team == 'Red':
            off_2er = rod_def[0]
            off_5er = rod_5er[0]
            off_3er = rod_3er[0]
            off_goal = goal[0]
            def_2er = rod_def[1]
            def_5er = rod_5er[1]
            def_3er = rod_3er[1]
            def_goal = goal[1]
        elif team == 'Blue':
            off_2er = rod_def[1]
            off_5er = rod_5er[1]
            off_3er = rod_3er[1]
            off_goal = goal[1]
            def_2er = rod_def[0]
            def_5er = rod_5er[0]
            def_3er = rod_3er[0]
            def_goal = goal[0]
        else: 
            exit()
        # total ball posession
        total = posession(time_pos, ball_pos, time_diff, off_2er)['counts']
        # positive offense play by 2 rod defense 
        retries = from_to(ball_pos, off_2er, off_2er)
        pass5er = from_to(ball_pos, off_2er, off_5er)
        pass3er = from_to(ball_pos, off_2er, off_3er)
        goals = from_to(ball_pos, off_2er, off_goal)
        # positive offense play by 2 rod defense 
        turnover_2er = from_to(ball_pos, off_2er, def_2er)
        turnover_5er = from_to(ball_pos, off_2er, def_5er)
        turnover_3er = from_to(ball_pos, off_2er, def_3er)
        own_goals = from_to(ball_pos, off_2er, def_goal)
        print total
        print retries, pass5er, pass3er, goals
        print turnover_2er, turnover_5er, turnover_3er, own_goals
        
        #print "result", rod
        #successes = 100.*rod['successes']/rod['total']
        #retries = 100.*rod['retries']/rod['total']
        #fails = 100.*(rod['total']-rod['successes']-rod['retries'])/rod['total']
        #fracs  = (successes, retries, fails)
        #print fracs
        #labels = (rod['successes'], rod['retries'], rod['total']-rod['successes']-rod['retries'])
        #plt.pie(fracs, labels=labels, shadow=True, colors=('g', 'b', 'r'))
    
    def from_to_statistics(team, active_rod):
        if team == 'Red':
            rod = team_red[np.where(team_rod==active_rod)[0]]
            off_2er = rod_def[0]
            off_5er = rod_5er[0]
            off_3er = rod_3er[0]
            off_goal = goal[0]
            def_2er = rod_def[1]
            def_5er = rod_5er[1]
            def_3er = rod_3er[1]
            def_goal = goal[1]
        elif team == 'Blue':
            rod = team_blu[team_rod==active_rod]
            off_2er = rod_def[1]
            off_5er = rod_5er[1]
            off_3er = rod_3er[1]
            off_goal = goal[1]
            def_2er = rod_def[0]
            def_5er = rod_5er[0]
            def_3er = rod_3er[0]
            def_goal = goal[0]
        else:
            exit()
        # total ball posession
        total = posession(time_pos, ball_pos, time_diff, rod)['counts']
        # positive offense play by 2 rod defense 
        pass2er = from_to(ball_pos, rod, off_2er)
        pass5er = from_to(ball_pos, rod, off_5er)
        pass3er = from_to(ball_pos, rod, off_3er)
        goals = from_to(ball_pos, rod, off_goal)
        total_off = pass2er + pass5er + pass3er + goals
        # positive offense play by 2 rod defense 
        turnover_2er = from_to(ball_pos, rod, def_2er)
        turnover_5er = from_to(ball_pos, rod, def_5er)
        turnover_3er = from_to(ball_pos, rod, def_3er)
        own_goals = from_to(ball_pos, rod, def_goal)
        total_def = turnover_2er + turnover_5er + turnover_3er + own_goals
        #print team, active_rod, '(', rod, ') = ', total
        #print total_off, '=', pass2er, pass5er, pass3er, goals
        #print total_def, '=', turnover_2er, turnover_5er, turnover_3er, own_goals
        return (own_goals, turnover_3er, turnover_5er, turnover_2er,
                pass2er, pass5er, pass3er, goals)

    # plot
    fig, ax = plt.subplots(figsize=(3, 3))#, dpi=100)
    fig.subplots_adjust(left=0.3, right=0.98, top=0.75, bottom=0.1)

    # Defense
    fracs  = from_to_statistics('Red', 'Defense')
    #(goals, pass3er, pass5er, pass2er,
    #        turnover_2er, turnover_5er, turnover_3er, own_goals)
    labels =  ('own goal', 'turnover 3er', 'turnover 5er', 'turnover_2er',
             'retry', 'pass 5er', 'pass 3er', 'goal')
    print fracs, labels
    colors=('r', 'tab:orange', 'y', 'y',
            '0.5', '0.5', 'b', 'g')
    plot_bar2(fracs, labels, colors, xpos=1.0, width=0.65, legend=True, ax=ax)

    #the_grid = GridSpec(2, 3)
    
    
    #plt.subplot(the_grid[0, 0], aspect=1)
    
    print ax 
    
    #print_rod_pie('Red', 'Midfield')
    #print_rod_pie('Red', 'Forward')
    #print_rod_pie('Blue', 'Defense')
    #print_rod_pie('Blue', 'Midfield')
    #print_rod_pie('Blue', 'Forward')
    
    
    
    
    
    
    # red offense
    #plt.subplot(the_grid[0, 0], aspect=1)
    #plt.title('red: 5-3')
    #plot_success_pie(4, 6)
    #plt.subplot(the_grid[1, 0], aspect=1)
    #plt.title('red: 3-goal')
    #plot_success_pie(6, 8)

    # blue offense
    #plt.subplot(the_grid[0, 1], aspect=1)
    #plt.title('blue: 5-3')
    #plot_success_pie(5, 3)
    #plt.subplot(the_grid[1, 1], aspect=1)
    #plt.title('blue: 3-goal')
    #plot_success_pie(3, 1)

    # red defense defense
    #plt.subplot(the_grid[0, 2], aspect=1)
    #plt.title('red: 3-catch')
    #plot_catch_pie(3, 2)
    #plt.subplot(the_grid[1, 2], aspect=1)
    #plt.title('blue: 3-goal')
    #plot_pie(3, 1)
    
    # defense offense
    #plt.subplot(the_grid[0, 3], aspect=1)
    #plt.title('red def')
    #plt.subplot(the_grid[1, 3], aspect=1)
    #plt.title('blue def')
    #plot_defense_pie(3, 1)
    

    # save
    save_name = 'out/' + file_name[4:-4] + '_success' + '.pdf'
    fig.savefig(save_name)
    print "evince", save_name, "&"

##########################################################################3
##########################################################################3
if __name__ == "__main__":
    # data
    arguments = docopt(__doc__, version='analyze trigger')
    file_name = arguments['--input']

    # proc data
    time_pos, ball_pos, ball_pos_raw, time_diff = proc_data(file_name)

    # plot timeline
    #plot_timeline(time_pos, ball_pos)

    # ball posession
    #plot_posession(time_pos, ball_pos, time_diff)

    # shoot/defense statistics
    plot_success(ball_pos, ball_pos_raw)

    # goals: rods and timeline
    #goals(ball_pos, 1)
