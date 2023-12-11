# src-ftbl-home-project

This project proposes an etl process for the src ftbl home project.  

I decided to use Google Cloud Platform to develop and run the etl process, indeed, 
processing our pipelines on a cloud provider offers us different benefits : 
- easy and secured access to the data  
- structured organizations
- connectivity to different tools 
- scalability
- cost efficiency

Our data system involved these followings tools :
- python, to develop our data system and transformations.
- sql, to transform and load data to our dataset.
- flask api, to define the different steps and jobs. 
- Google Cloud Storage, use here as a datalake to store our raw data.
- Google Cloud Bigquery, the data warehouse choose where the user can access the data.
- Cloud run, to compute and process the application.
- Cloud workflows, to orchestrate our data pipeline.
- Github, the version control tool for the project.
- Github actions, the ci/cd tool.
- Terraform, create and manage the app infrastructure.
- Docker, to make our app reproducible on other structure.

This system has several advantages, first of all it is cost efficient, cloud run only works when the app is triggered, 
once the job is finished, the cloud run service stop.
Docker allows us to containerize our app and make it easy to deploy. We use a ci/cd workflow to build and deploy our app,
potentially we can add another ci/cd workflow to deploy our app on different environments (dev/prep and prod), I didn't add it here,
because I thought it wasn't a primary need here. 
Beside that, I use the cloud workflow tool from gcp, it is a small and cheap orchestration tool, 
I use it to orchestrate our ETL process, if we need to scale I think this orchestration tool would show some limits, 
especially regarding the monitoring of the pipelines. 

## Data model 
You will find in the `install/schema` folder the 3 tables schema I designed. 
I thought about differents data model, first I planned to create an all database with tables about teams, players, seasons, leagues, stadium...
And I realized that it wasn't necessary to have all these informations in this case, so I decided to go with 3 differents tables : 
- game_tracking, we find the tracking data normalized with he game id added to make it easier working the game informations.
- game_summary, the game basics informations based on the metadata table
- game_players_summary, we have in this table the game first statistics for each player of the game.

I chose a relational database schema as it provides a structured and organized way to store data, making it easier
for the data science team to query and analyze.

## Alternatives

When exploring alternatives, I contemplated the use of NoSQL databases to enhance flexibility with unstructured data. 
However, for analytical purposes, opting for a relational schema proved more advantageous due to its ease of use and structured nature.

Regarding running time, acknowledging the potential benefits of code optimization is paramount. 
While a comprehensive code review and optimization were not feasible within the given timeframe, 
it remains a crucial avenue for improving overall efficiency.

In terms of compute cost, the current implementation utilizing Cloud Run stands out for its cost-effectiveness. 
As the number of processes and ETL jobs grows, a strategic transition to tools like Apache Airflow could be considered. 
Although it introduces certain costs, its ability to streamline ETL jobs and development might outweigh the expenditure.

Addressing storage costs involves optimizing both Cloud Storage and BigQuery. 
Adjusting the bucket type and access permissions can contribute to cost reduction. 
BigQuery tables are already optimized with partitioned fields and clustered tables, minimizing data retrieval during queries.

To handle scalability concerns, the current strategy involves incorporating partitioning and clusters within tables. 
While effective for smaller processes, scaling raises considerations about orchestration tools. 
Exploring alternative orchestration tools could significantly enhance pipeline monitoring and alerting systems, particularly as the data system expands.

In the context of merging data with event data, establishing a common key between datasets is imperative. 
Introducing the player ID into the game tracking table, coupled with a timestamp, could serve as a potential key. 
Alternatively, if there exists an event ID that aligns between datasets, it would offer an ideal solution for seamless integration. 
This step not only ensures data compatibility but also facilitates a more comprehensive analysis by linking pertinent information across different sources.

### Task 2

In the pursuit of identifying the five most intense minutes for each player, three primary factors were considered:

#### Key Metrics:  
**Distance:**  
Definition: Reflects the spatial coverage of each player across the pitch.
Calculation: Total distance covered by a player within a specific time interval.  

**Speed:**  
Definition: Represents the rate at which a player moves from one point to another.
Calculation: Derived as the distance traveled divided by the time taken, providing a comprehensive view of the player's overall pace.  

**Acceleration:**  
Definition: Measures the change in speed over time, capturing the player's dynamic movements.
Calculation: Quantifies how rapidly a player accelerates or decelerates during specific actions.  

####Additional Considerations:

While the primary focus involved these core metrics, there were contemplations regarding further factors that could enhance the intensity determination. These considerations included:

**Distance with the Ball:** Proximity to the ball and player movement in possession situations.

**Position on the Pitch:** Acknowledging the impact of player positions on their perceived intensity.

**Game Situation and Time:** Understanding the contextual factors related to the current state of the game and the specific timeframe.

Despite these considerations, the implementation of these additional factors was deferred due to time constraints. 
It is recognized that certain scenarios, such as a defensive strategy in the closing minutes of a game, 
might result in intense moments not fully captured by distance, speed, and acceleration metrics alone.

In particular, the last five minutes of a game, 
even if characterized by a defensive stance, may be the most intense for defenders and attackers alike. 
However, this intensity might not align with traditional metrics, 
highlighting the importance of considering contextual elements for a more nuanced analysis.

In conclusion, while the current focus lies on fundamental player metrics, 
the potential inclusion of additional factors remains an avenue for future exploration, 
promising a more holistic understanding of player intensity under varied game conditions.

For the spread metric, I tried to first calculate it with the ball for each player and then expand it to each player,
I couldn't verify it statistically but intensity and spread metrics should be related because the distance is a key factor to measure the intensity.
More the players are far from each other, more they make efforts to play and move together as a team, so it multiplies intensive moments. On the other hands, 
if the players manage to stay close to each other, less distance they have to cover individually, efforts are less intense because of the distance covered by theam and not by a player individually.


As it was the first time I use spark, I struggled a bit to make my code working and was not able to compute the results.  
You will find the code here : `app/src/services` and the app code is in the `main.py`at the root of the project.