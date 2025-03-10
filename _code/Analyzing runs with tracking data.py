# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:11:40 2024

@author: henri
"""
import json
import os
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=25, codec='libx264', extra_args=['-pix_fmt', 'yuv420p'])

import pandas as pd
from matplotlib.animation import FuncAnimation
from mplsoccer import Pitch

path_to_folder = r"C:\Users\henri\Desktop\Sm\Tracking data\18768058_tracking.json"
match_id = 18768058

# Read tracking data file line-by-line
data = []
with open(path_to_folder, 'r') as f:
    for line in f:
        obj = json.loads(line.strip())  # Parse each line as JSON
        data.append(obj)
print(len(data))

df_test = data[118200:118495] # Frame for Foden chance
df_test2=data[7150:7500]
#første omgang end: frame 70396
# Slice for hendelsene
# Konverter hver liste til en DataFrame

custom_data = []
for d in df_test2:
    for p in d['players']:
        custom_data.append({
            'time': d.get('time'),
            'frame': int(d.get('frame_id')),
            'period': int(d.get('period')[-1]),
            'person_id': p.get("person_id"),
            'player': p.get('person_name'),
            'team_name': p.get('team_name'),
            'jersey_number': p.get("jersey_number"),
            'x': p.get('x'),
            'y': p.get('y'),
            'x_velocity': p.get('x_velocity'),
            'y_velocity': p.get('y_velocity'),
            'speed': p.get('speed'),
            'x_acceleration': p.get('x_acceleration'),
            'y_acceleration': p.get('y_acceleration'),
            'acceleration': p.get('acceleration'),
        })
    #Add the ball
    ball = d.get('ball')
    custom_data.append({
        'time': d.get('time'),
        'frame': int(d.get('frame_id')),
        'period': int(d.get('period')[-1]),
        'person_id': -100,
        'player': 'ball',
        'team_name': 'ball',
        'jersey_number': -1,
        'x': ball.get('x'),
        'y': ball.get('y'),
        'x_velocity': ball.get('x_velocity'),
        'y_velocity': ball.get('y_velocity'),
        'speed': ball.get('speed'),
        'x_acceleration': ball.get('x_acceleration'),
        'y_acceleration': ball.get('y_acceleration'),
        'acceleration': ball.get('acceleration')
    })
df_frames = pd.DataFrame(custom_data)
#Create custom unique frame_ids -> add 100000 to the frame of period 2
#df_frames.loc[df_frames['period'] == 2, 'frame'] += 100000
flip_y = True
# For plotting purposes, we flip the y-coordinates (and speed and acceleration)
if flip_y:
    df_frames['y'] = 68 - df_frames['y']
    df_frames[['y_velocity','y_acceleration']] = -1*df_frames[['y_velocity','y_acceleration']]
    flip_y = False

# Note that to make this work, you might need to download and configure ffmpeg:
# https://www.ffmpeg.org/download.html
# Guide to set it to environmental variables:
# https://www.youtube.com/watch?v=r1AtmY-RMyQ&ab_channel=TroubleChute

# Plot function for each frame 
def update(frame_id):
    ax.clear()
    pitch.draw(ax=ax)  # Redraw the pitch for each frame
    
    frame_data = frames.get_group(frame_id)
    
    #Set properties for the teams and the ball
    teams = {
        'Manchester City':{
            'color': "skyblue", 'size':150},
        'Inter':{
            'color': "blue", 'size':150},
        'ball':{
            'color': "black", 'size':50},
        }

    # Plot each player as a scatter point - Inter as dark blue, City lightblue
    for team, props in teams.items():
        ax.scatter(
            frame_data[frame_data['team_name'] == team]['x'], 
            frame_data[frame_data['team_name'] == team]['y'], 
            s=props['size'], 
            color=props['color'], 
            zorder=5
        )
        
        # Add velocity arrows for each team with specified arrow color
        ax.quiver(
            frame_data[frame_data['team_name'] == team]['x'], 
            frame_data[frame_data['team_name'] == team]['y'],
            frame_data[frame_data['team_name'] == team]['x_velocity'], 
            frame_data[frame_data['team_name'] == team]['y_velocity'],
            angles='xy', scale_units='xy', scale=2, color=props['color'], width=0.003, zorder=4
        )
    
    
    
    # Add jersey numbers on the players
    for _, row in frame_data.iterrows():
        if row['team_name'] != 'ball':
            ax.text(row['x'], row['y'], str(row['jersey_number']), color="white", 
                    ha="center", va="center", fontsize=8, weight="bold", zorder=6)
            
    # Retrieve the game time and period from the frame data
    game_time = frame_data['time'].iloc[0][0:5]  
    period = frame_data['period'].iloc[0]
    
    # Display the game time and period on top of the pitch
    ax.text(
        52.5, 72, f"Period {period} - Time {game_time}", 
        ha="center", va="center", fontsize=15, color="black", fontweight="bold", 
    )

#%%
#Create custom unique frame_ids -> add 100000 to the frame of period 2
df_frames.loc[df_frames['period'] == 2, 'frame'] += 100000
#Select the frames to plot
frame_min = 
frame_max1= 33734
frame_min1=33799
#frame_max2=33800
#frame_min2=33808
frame_max = 34183

df = df_frames[(df_frames.frame > frame_min) & (df_frames.frame < frame_max)]

# Create the pitch
pitch = Pitch(pitch_type='uefa')
fig, ax = pitch.draw(figsize=(10, 7))

# Group data by frame for easier access
frames = df.groupby('frame')
# Create the animation
frame_ids = sorted(df['frame'].unique())
anim = FuncAnimation(fig, update, frames=frame_ids, repeat=False)

# Save the animation as an mp4 video - The data is collected at 25 fps
# You can slow down or speed up the video by changing the fps variable.
output_path = r"C:\Users\henri\Desktop\Ballprog\Spyder\city_inter.mp4"
anim.save(r"C:\Users\henri\Desktop\Ballprog\Spyder\city_inter.mp4", writer=writer)

#anim.save('city_inter.mp4', fps=25)

#anim.save(output_path, fps=25)

#print(len(df))
#print(df.head())

#print(frame_ids)


#diffs = np.diff(frame_ids)
#print(diffs)

def update(frame_id):
    ax.clear()
    pitch.draw(ax=ax)  # Redraw the pitch for each frame
    
    frame_data = frames.get_group(frame_id)
    
    # Set properties for the teams and the ball
    teams = {
        'Manchester City': {'color': "skyblue", 'size': 150},
        'Inter': {'color': "blue", 'size': 150},
        'ball': {'color': "black", 'size': 50},
    }

    # Plot each player as a scatter point
    for team, props in teams.items():
        ax.scatter(
            frame_data[frame_data['team_name'] == team]['x'], 
            frame_data[frame_data['team_name'] == team]['y'], 
            s=props['size'], 
            color=props['color'], 
            zorder=5
        )
        
        # Add velocity arrows for each team
        ax.quiver(
            frame_data[frame_data['team_name'] == team]['x'], 
            frame_data[frame_data['team_name'] == team]['y'],
            frame_data[frame_data['team_name'] == team]['x_velocity'], 
            frame_data[frame_data['team_name'] == team]['y_velocity'],
            angles='xy', scale_units='xy', scale=2, color=props['color'], width=0.003, zorder=4
        )
    
    # Add jersey numbers and specific text for Bernardo Silva
    for _, row in frame_data.iterrows():
        if row['team_name'] != 'ball':
            ax.text(row['x'], row['y'], str(row['jersey_number']), color="white", 
                    ha="center", va="center", fontsize=8, weight="bold", zorder=6)
        
        if row['player'] == 'Jack Grealish':
            ax.text(row['x'] + 1, row['y'], "Grealish", color="black", 
                    ha="left", va="center", fontsize=10, weight="bold", zorder=6)
    
    # Retrieve the game time and period from the frame data
    game_time = frame_data['time'].iloc[0][0:5]  
    period = frame_data['period'].iloc[0]
    
    # Display the game time and period on top of the pitch
    ax.text(
        52.5, 72, f"Period {period} - Time {game_time}", 
        ha="center", va="center", fontsize=15, color="black", fontweight="bold", 
    )

frame_min = 7199
frame_max = 7548

df = df_frames[(df_frames.frame > frame_min) & (df_frames.frame < frame_max)]

# Create the pitch
pitch = Pitch(pitch_type='uefa')
fig, ax = pitch.draw(figsize=(10, 7))

# Group data by frame for easier access
frames = df.groupby('frame')

# Create the animation
frame_ids = sorted(df['frame'].unique())
anim = FuncAnimation(fig, update, frames=frame_ids, repeat=False)

# Save the animation as an mp4 video
#output_path = r"C:\Users\henri\Desktop\Ballprog\Spyder\city_inter.mp4"
#anim.save(output_path, writer=writer)
