# src-ftbl-home-project

This project proposes an etl process for the src ftbl home project.  

I decided to use Google Cloud Platform to develop and run the etl process, indeed, 
processing our pipelines on the cloud offers us different benefits : 
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

This system has several advantages, first of all it is cost efficient, cloud run only works when the app is triggered, once the job is finished, the cloud run service stop.
Docker allows us to containerize our app and make it easy to deploy. We use a ci/cd workflow to build and deploy our app, 

# schema 


#CI/CD workflows

### final data 
After a look at the data, I started designing the data model to expose our informations to ou
