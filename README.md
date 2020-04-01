# My stupid attempt at modeling the coronavirus outbreak
#### Author : Ali Snedden
#### License: MIT 
## Purpose:
I'm curious if I can predict the outbreak behavior with an agent based model. This is a really ignorant attempt at modeling and I have no experience in these type of simulations.

## Installation:
Use a python 3 installation that includes common libraries such as numpy and matplotlib

## Usage:
This repo does several things.
1. It plots and fits the Itallian covid-19 data from the [national government](https://github.com/pcm-dpc/COVID-19.git). E.g. (fitting the last 10 points) : 
   `python src/plot_italy_data.py [option_to_plot] data/dpc-covid19-ita-andamento-nazionale.csv log-lin -10`
2. It plots the country cases (see [John Hopkins' data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)) as a function of time. E.g. (fitting the last 10 points) : 
    `python src/plot_jhu_data.py us log-lin -10`

3. It plots several countries' death data (see [John Hopkins' data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)) showing 1 day and 3 day doubling times. E.g.
    `python src/plot_country_deaths.py`


#### References:
1. [Strategies for mitigating an influenza pandemic](https://www.nature.com/articles/nature04795#Sec2)
2. [Impact of non-pharmaceutical interventions (NPIs) to reduce COVID- 19 mortality and healthcare demand](https://spiral.imperial.ac.uk:8443/handle/10044/1/77482)
3. [Italian Department of Civil Protection](https://github.com/pcm-dpc/COVID-19.git)
