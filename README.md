# My stupid attempt at modeling the coronavirus outbreak
#### Author : Ali Snedden
#### License: MIT 
## Purpose:
This is a really ignorant attempt at understanding covid19.  I have no experience in these type of simulations or analyzing this kind of data.  This repos contains programs that do modeling and plotting

## Installation and Dependencies :
1. Python 3 installation that includes common libraries such as numpy and matplotlib.
2. ffmpeg - Only useful for generating movies from the simulations

## Usage:
This repo does several things.
1. It plots and fits the Itallian covid-19 data from the [national government](https://github.com/pcm-dpc/COVID-19.git). E.g. (fitting the last 10 points) : 

```
python3 ./src/plot_italy_data.py option_to_plot italy_data_file [log-lin] [index]
      option_to_plot :
           'hosp_w_sympt'  : Hospitalized w/ Symptoms
           'icu'           : Intensive Care Units
           'total_hosp'    : All Hospitalized
           'home_isolation': Home Isolation
           'total_positive': All Positive
           'new_positive'  : New Positive
           'discharged'    : Discharged
           'dead'          : Dead
           'total_cases'   : Total Cases
           'swabs'         : Swabs
      italy_data_file : the path to the dpc-covid19-ita-andamento-nazionale.csv
      [log-lin or lin-lin] : optional, plot y axis in natural log, if straight line
                             then experiencing exponential growth. If not specified,
                             log-lin assumed
      [slice_index]        : for fitting, e.g.
                             if = -10, it will fit the last 10 points
                             if = 10, it will fit the first 10 points
```


2. It plots the country cases (see [John Hopkins' data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)) as a function of time. E.g. (fitting the last 10 points) : 

    `python src/plot_jhu_data.py us log-lin -10`

3. It plots several countries' death data (see [John Hopkins' data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)) showing 1 day and 3 day doubling times. Motivated by [NYT plot](https://www.nytimes.com/interactive/2020/03/21/upshot/coronavirus-deaths-by-country.html).  E.g.

    `python src/plot_country_deaths.py [quarantine]`

4. I created a fun little toy program that emulates the type of plotting / simulations done in [Simulating an Epidemic - YouTube](https://www.youtube.com/watch?v=gxAaO2rsdIs). 

    `python simulating_epidemic_youtube.py`

    To generate the movie : 

    `ffmpeg -framerate 4 -pattern_type glob -i 'output/*.png' -c:v libx264 out.mp4`

<!-- 5. Mention Runge-Kutta integration of DE's from OSU/IDE paper -->

#### References:
1. [Strategies for mitigating an influenza pandemic](https://www.nature.com/articles/nature04795#Sec2)
2. [Impact of non-pharmaceutical interventions (NPIs) to reduce COVID- 19 mortality and healthcare demand](https://spiral.imperial.ac.uk:8443/handle/10044/1/77482)
3. [Italian Department of Civil Protection](https://github.com/pcm-dpc/COVID-19.git)
4. [Institute for Health Metrics and Evaluation](https://covid19.healthdata.org/united-states-of-america)
5. [Estimating the asymptomatic proportion of coronavirus disease 2019 (COVID-19) cases on board the Diamond Princess cruise ship](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7078829/)
6. [Simulating an Epidemic - YouTube](https://www.youtube.com/watch?v=gxAaO2rsdIs)
