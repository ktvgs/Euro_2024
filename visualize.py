import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

df1=pd.read_csv('euro_players_stats_final.csv')

df1['fixture_id'] = df1['fixture_id'].astype(str)

fixtures=pd.read_csv('euro_2024_fixtures.csv')

def player_rating_plot(player_id):
    # Columns for analysis including position
    df = df1
    cols = ['player_id', 'team_name', 'stat_games_rating', 'fixture_id', 'player_name', 'stat_games_position']
    
    # Filter data for the specific player
    player_data = df[df['player_id'] == player_id][cols]

    # Filter data for the rest of the team in the same fixtures
    team_data = df[(df['fixture_id'].isin(player_data['fixture_id'])) & 
                   (df['team_name'] == player_data.iloc[0]['team_name']) &
                   (df['player_id'] != player_id)][cols]

    # Convert fixture_id to the same type in both DataFrames
    player_data['fixture_id'] = player_data['fixture_id'].astype(str)
    team_data['fixture_id'] = team_data['fixture_id'].astype(str)
    fixtures['fixture_id'] = fixtures['fixture_id'].astype(str)

    # Merge player_data and team_data with fixtures_df to get round information
    player_data = player_data.merge(fixtures[['fixture_id', 'round']], on='fixture_id', how='left')
    team_data = team_data.merge(fixtures[['fixture_id', 'round']], on='fixture_id', how='left')

    # Set 'fixture_id' as index for both player and team data
    player_data.set_index('fixture_id', inplace=True)
    team_data.set_index('fixture_id', inplace=True)

    # Create custom x-labels using round information
    rounds = player_data['round'].tolist()

    # Define position-based color mapping
    position_colors = {
        'G': 'red',
        'D': 'green',
        'M': 'orange',
        'F': 'purple'
    }
    
    # Plot the player's rating with thicker line, larger markers, and solid line
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, player_data['stat_games_rating'], marker='o', color='blue', 
             label=f"{player_data.iloc[0]['player_name']}'s Rating", linewidth=3, markersize=10, linestyle='-')

    # Keep track of plotted positions to avoid duplicate legends
    plotted_positions = set()

    # Plot the teammates' ratings with color coding based on position and dashed line
    for player in team_data['player_id'].unique():
        player_team_data = team_data[team_data['player_id'] == player]
        position = player_team_data.iloc[0]['stat_games_position']
        color = position_colors.get(position, 'gray')  # Default color is gray if position is missing
        
        # Create rounds for each teammate based on their data
        rounds_team = player_team_data['round'].tolist()
        
        # Plot each teammate's rating with a dashed line and smaller markers
        plt.plot(rounds_team, player_team_data['stat_games_rating'], marker='o', color=color, alpha=0.6,
                 linewidth=1, markersize=6, linestyle='--')

        # Add the position to the legend only once
        if position not in plotted_positions:
            plt.plot([], [], marker='o', color=color, label=f'{position}')  # Add position to the legend
            plotted_positions.add(position)

    # Add x-ticks as Round labels
    plt.xticks(rotation=45)

    # Titles and Labels
    plt.title(f'Player and Teammates Ratings for {player_data.iloc[0]["player_name"]}')
    plt.xlabel('Round')
    plt.ylabel('Rating')
    plt.grid(True)
    plt.tight_layout()
    plt.legend(title='Position')
    plt.show()


# Example usage:
# player_rating_plot(752, df)


df2=pd.read_csv('Data/euro_final.csv')



# Define the function
def plot_player_radar_with_stats(player_id ):
    # Filter the DataFrame for the given player_id
    df = df2
    player_id = int(player_id)
    print(type(player_id))
    player_data = df[df['id'] == player_id]
    
    if player_data.empty:
        print(f"No data found for player ID {player_id}")
        return
    
    # Get the player's position and filter DataFrame for that position with >=5 appearances
    player_position = player_data.iloc[0]['games_position']
    df_filtered = df[(df['games_position'] == player_position) & (df['games_appearences'] >= 5)]
    
    # Define the attributes for radar chart
    attributes = ['passes_accuracy', 'goals_assists', 'passes_key', 'games_rating']
    
    # Scale 'passes_accuracy' out of 10 for the player and the statistics
    player_data['passes_accuracy'] = player_data['passes_accuracy'] / 10
    
    # Extract player's values
    player_values = player_data[attributes].values.flatten()  # Get values as a flat array
    
    # Compute summary statistics for comparison
    summary_stats = df_filtered[attributes].describe()  # Compute stats for the filtered attributes
    
    # Scale 'passes_accuracy' out of 10 in the summary stats
    summary_stats.loc['min', 'passes_accuracy'] /= 10
    summary_stats.loc['25%', 'passes_accuracy'] /= 10
    summary_stats.loc['50%', 'passes_accuracy'] /= 10
    summary_stats.loc['75%', 'passes_accuracy'] /= 10
    summary_stats.loc['max', 'passes_accuracy'] /= 10
    summary_stats.loc['mean', 'passes_accuracy'] /= 10

    # Get the stats values for the radar plot
    min_values = summary_stats.loc['min', attributes].values
    max_values = summary_stats.loc['max', attributes].values
    percentile_75_values = summary_stats.loc['75%', attributes].values
    mean_values = summary_stats.loc['mean', attributes].values
    
    # Number of variables
    num_vars = len(attributes)
    
    # Compute angles for the radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Append the first value again to close the radar plot
    player_values = np.concatenate((player_values, [player_values[0]]))
    min_values = np.concatenate((min_values, [min_values[0]]))
    max_values = np.concatenate((max_values, [max_values[0]]))
    percentile_75_values = np.concatenate((percentile_75_values, [percentile_75_values[0]]))
    mean_values = np.concatenate((mean_values, [mean_values[0]]))
    angles += angles[:1]
    
    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Plot each line with different colors and fading
    ax.fill(angles, player_values, color='blue', alpha=0.4, label='Player')
    ax.plot(angles, player_values, color='blue', linewidth=2, linestyle='solid')

    ax.fill(angles, min_values, color='green', alpha=0.1, label='Min')
    ax.plot(angles, min_values, color='green', linewidth=1, linestyle='dotted')

    ax.fill(angles, max_values, color='red', alpha=0.1, label='Max')
    ax.plot(angles, max_values, color='red', linewidth=1, linestyle='dashdot')

    ax.fill(angles, percentile_75_values, color='purple', alpha=0.1, label='75%')
    ax.plot(angles, percentile_75_values, color='purple', linewidth=1, linestyle='dashed')

    ax.fill(angles, mean_values, color='cyan', alpha=0.1, label='Mean')
    ax.plot(angles, mean_values, color='cyan', linewidth=1, linestyle='solid')

    # Add attribute labels
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)
    
    # Title and legend
    player_name = player_data.iloc[0]['name']  # Assuming 'name' is in the DataFrame
    plt.title(f"Radar Chart for {player_name} with Summary Stats", size=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
    # Show the radar chart
    plt.show()
    
    

# Example usage
# Call the function with a player ID (make sure to pass your DataFrame `df_filtered`)
# plot_player_radar_with_stats(player_id=752, df=df2)
