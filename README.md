# AthleteLoadMonitor
**Load Monitoring and Prediction tool for Team Sports Coaches**

This tool helps coaches of sports teams (soccer, field hockey) to gain insight in the fitness of their players. It combines data gathered from sensors during a training (e.g. acceleration, speed, distance, heart rate) with questionnaire data (e.g. wellbeing and Rated Perceived Exertion). Trends in this data can be visualized in the tool and can be used to make decisions on the training schedule of the athletes.

| <p align="center"><img src="https://github.com/SaxionAMI/AthleteLoadMonitor/raw/main/resources/player_list.png"></p> |
|:--:|
|  *Player overview per team*                                                                                                                     |

|<p align="center"><img src="https://github.com/SaxionAMI/AthleteLoadMonitor/raw/main/resources/hs_distance_plot.png" width="600"></p>|
|:--:|
| *Detail graph of one parameter; all parameters are configurable*    |

The Athlete Load Monitor also has the capability to create predictive models on some variables. The Rated Perceived Exertion (RPE) is a good candidate to use. If the predictions of this variable deviate highly from the actual values the athletes write down in their survey, this could indicate that the player is not as fit as he / she should be. A high deviation is shown as a high risk in the tool.

| <p align="center"><img src="https://github.com/SaxionAMI/AthleteLoadMonitor/raw/main/resources/rpe_plot.png" width="600"></p> |
| ----------------------------------------------------------------------------------------------------------------------------- |
|  *RPE graph with predictions*                                                                                                                              |

The tool is highly configurable with a bit of programming knowledge. Different sports clubs use different systems for tracking their players (e.g. Polar, ZXY Go, Statsports Apex) and different formats to write down the results of the questionnaires (Excel, .csv etc). The structure of the projects allows these various data sources to be combined.

| <p align="center"><img src="https://github.com/SaxionAMI/AthleteLoadMonitor/raw/main/resources/import.png" width="600"></p> |
| ------------------------------------------------------------------------------------------------------------------------------------- |
| *Importing different types of data sources*                                                                                                                                      |

As it often happens that players have slightly different names in the different sources, a mapping utility has been implemented to reconcile the different names.

| <p align="center"><img src="https://github.com/SaxionAMI/AthleteLoadMonitor/raw/main/resources/manage_trainings.png" width="600"></p> |
| ------------------------------------------------------------------------------------------------------------------------------------- |
| *Mapping player names and creating new prediction models*                                                                                                                                      |



See [the wiki pages](https://github.com/SaxionAMI/AthleteLoadMonitor/wiki) for the technical documentation and instructions how to set up the system.
