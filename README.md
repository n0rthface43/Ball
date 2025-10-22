# SkillCorner Open Data

## About this repo

### Description

This repo contains data on 10 matches of broadcast tracking data collected by [SkillCorner](https://skillcorner.com), as well as a dataset on aggregated Physical data at the season level.

The matches included are a sample of 2024/2025 league matches in the Australian A-League

Broadcast tracking data is tracking data collected through computer vision and machine learning out of the broadcast video.


### Motivation

This data has been open sourced in a joint initiative between [SkillCorner](https://skillcorner.com) and [PySport](https://pysport.org/). The goals are multiple:
* Provide access to tracking data to researchers and the sports analytics community.
* Increase awareness on the existence of broadcast tracking data, and how it can be of benefit to clubs, media and the betting industry.
* Allow SkillCorner prospects to access data easily, parse our data format and get started building on top of it.

Thus, if you use the data, we kindly ask that you credit SkillCorner and hope you'll notify us on [Twitter](https://twitter.com/skillcorner) so we can follow the great work being done with this data.

## Documentation

### Data Structure

The `data` directory contains:

* `matches.json` file with basic information about the match. Using this file, pick the `id` of your match of interest.
* `matches` folder with one folder for each match (named with its `id`).
* `aggregates` folder with a csv for the season level, aggregated data for AUS midifielders in 2024/2025.

For each match, there are four files files:

* `{id}_match.json` contains lineup information, time played, referee, pitch size...
* `{id}_tracking_extrapolated.jsonl` contains the tracking data (the players and the ball).
* `{id}_dynamic_events.csv` contains our Game Intelligence's dynamic events file (See further for specs.)
* `{id}_phases_of_play.csv` contains our Game Intelligence's PHASES OF PLAY framework file. (See further for specs.)

#### Tracking Data Description

The tracking data is a list. Each element of the list is the result of the tracking for a frame, it's a dictionary with keys:


* frame: the frame of the video the data comes from at 10 fps.
* timestamp: the timestamp in the match time with a precision of 1/10s.
* period: 1 or 2.
* ball_data: the tracking data for the ball at this frame. Dictionary
* possession: dict with keys player_id and group which indicates which player/team (home or away team) are in possession
* image_corners_projection: coordinates of polygon of the detected area. 
* player_data: list of information of the players at the given frame.  

Each element of the player_data list is a player found at this frame. It's a dictionary with keys:

* x: x coordinate of the object
* y: y coordinate of the object
* player_id: identifier of the player
* is_detected: flag that mentions if the player is detected on the screen or extrapolated


For the spatial coordinates, the unit of the field modelization is the meter, the center of the coordinates is at the center of the pitch.

The x axis is the long side and the y axis in the short side.

Here is an illustration for a field of size 105mx68m.
![Field modelization for a pitch of size 105x68](resources/field.jpg)

### Physical Data (Aggregates)

The physical data is aggregated at a player-group-season level and contains the key metrics from our physical data. [documentation here](https://skillcorner.crunch.help/en/glossaries/physical-data-glossary)
The dataset is filtered for performances above 60 mins only (sub players wouldn't appear unless they've played more than 60mins)


#### Dynamic Event Data

The dynamic_events data is a CSV. Each row corresponds to a specific event_id belonging to 4 subcategories.
Note:
* an event_id is unique *to a game only*
* the x/y attributes of each event are not scaled to standard pitchsize and require adjustement

For a full documentation of dynamic_events, refer to this [documentation here](https://26560301.fs1.hubspotusercontent-eu1.net/hubfs/26560301/Guides/Dynamic%20Events/20250216%20-%20Dynamic%20Events%20CSV%20Specifications.pdf)

#### Phases of Play File

The phase of play data is CSV. Each row corresponds to the start and end frames of a given phase

* Phases of play capture which phase the attacking and defending team are in concurrently.
* Phases of play are only defined when the ball is in play. When the ball is out of play there is no phase of play
* Each in-possession phase directly corresponds to an out-of-possession phase.

For detailed information on phases of play, refer to this [documentation](https://26560301.fs1.hubspotusercontent-eu1.net/hubfs/26560301/Guides/Phases%20of%20Play/20250216%20-%20Phases%20of%20Play%20CSV%20Specifications.pdf)

### Limitations

#### TRACKING
* Some data points are erroneous. Around 97% of the player identity we provide are accurate.
* Some speed or acceleration smoothing and control should be applied to the raw data.

## Working with the data

In the `Resources` folder, we've provided an array of code and notebooks that provides a starting point to work with the tracking data. To get started visit the Kloppy tutorial or dive into the Tutorials Folder. SkillCorner customers will also find commented code they can use to connect to their match_ids using their credentials.

Onlines version are available as well for:
* TRACKING Notebook: [GoogleColab](https://colab.research.google.com/drive/16JTBpuoDFoZ-PRiztLX4CPZmCatKtem7).
* SKILLCORNER VIZ visualization Library: [GoogleColab](https://colab.research.google.com/drive/1-uD-kWH7ya-PyG585L2qymVcQrBTtjFo#scrollTo=z5B8GqPiCGan)

## Future works

* We'll be hosting a hackathon in collaboration with [PySport](pysport.org/analytics-cup) !
* We intend to open source more tooling to help people get started with our data.
* We are not an event data provider ourself, though we intend to provide some tools to synchronize tracking and event data, that you'll be able to use if you can access event data.

## Contact us

* If you have some feedback, some project research that you want to conduct with our data, reach us on [our website](https://skillcorner.com/#contact-section) or on [Twitter](https://twitter.com/skillcorner)
* If you're interested in our product and want more commercial information contact us on [our website](https://skillcorner.com/#contact-section)
