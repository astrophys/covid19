<!--
Compile : 
    pandoc -f markdown -t latex -o covid-19_notes.pdf
    pandoc --biblio=notes/covid19.bib -f markdown notes/covid-19_notes.md --filter pandoc-crossref -t latex -o notes/output.pdf

Notes:
    1. http://lierdakil.github.io/pandoc-crossref/ 
    2. https://pandoc.org/MANUAL.html#bullet-lists
--> 
\newcommand{\overbar}[1]{\mkern 1.5mu\overline{\mkern-1.5mu#1\mkern-1.5mu}\mkern 1.5mu}


<!--
    YAML section
--> 
---
title: Notes on Covid-19 modeling
author: Ali Snedden
date: 2020-03-19
abstract: 
...

\maketitle
\tableofcontents
\pagebreak

[@ferguson20]
--------------
1. Transmission Model 
    a) Initial Conditions
        #.  Individuals reside in areas defined by high-resolution population density data 
        #.  Contacts are made within household, school and workplace
        #.  Use Census data used to create synthetic populations of schools distributed proportional to population density
        #.  Data on distribution of workplace size was used to generate workplaces with commuting distance data used to locate workplaces across the population.
        #.  Individuals assigned to locations at start of simulation.

    #) Transmission events
        #. Occurs through contacts made between susceptible and infections individuals
            * Based on household, workplace, school or randomly in community
                + Community based transmission is 'random'
            * Infection rate at schools is double what it is elsewhere
        
        #. One third of transmission occurs in household, one third in schools/workplaces, and third in community.
            * Contact patterns match social mixing surveys.

    #) The Virus
        #. Assumed incubation period of 5.1 days. 
        #. Infectiousness assumed to occur 12hours before onset of symptoms
        #. Asymptomatic incubation time is 6.5 days
        #. Symptomatic people are 50% more infectious than asymptomatic
        #. Describe individual infectiousness as described by a Gamma function with mean = 1 and shape ($$\alpha$$) = 0.25
        #. Assumed to be immune after infection

    #) Disease Progression and Healthcare demand
        #. Assumed that doubling time = 5 days
        #. Assumed 40-50% of infections were not identified in China
            * Includes :
                + Asymptomatic
                + Mild cases
                + Under-ascertainment
        #. Assume 2/3 are sufficiently symptomatic to self-isolate within 1 day of symptom onset.
        #. Mean delay of onset of symptoms to hospitalization = 5 days.
        #. IFR (Infection Rate Mortality = 0.9% 
        #. 4.4% of cases hospitalised
        #. 30% of hospitalized cases will require critical care.
        #. Assume 8 days of hospitalization w/o critical care. 16 days if critical care reqr'd.
            * 10 days in ICU if critical care needed.
        #. 50% of critical care die (expert opinion)
        #. Table 1 provides IFR for different populations.

    


[@osuidi20]
--------------
1. Methods 
    a) Dynamic Network Model - see [@newman18]
        #. Nodes represent people and edges represent connection through proximity
        #. Three distinguishing features of statewide model
            * Model supports dynamic network where edges can be deactivated over time.
                + Reflect social distancing impacts more accurately.
            * Use law of large numbers to derive set of differential equations that describe disease process on a large network w/o requiring simulation methods
            * Solutions to DE's can be used to est. model params using principled statistical approach base on survival analysis. 
                + Permits more accurate quantification of uncertainty.
                + See [@khudabukhsh19]
        #. Use age distribution of county to predice how many hospitalizations will occur.
            * Assumes the distribution of new infections is uniform across age distribution

    #) Detailed Methods of Statewide Model
        #. Challenges of traditional compartmentel models
            * If using the entire population, can over-estimate
            * Lack of data on mild / asymptomatic infection is problematic
        #. Use "Dynamic Survival Analysis" [@bastian20]
        #. Advantages, does not require : 
            * Knowing the size of the susceptible population
            * Overall disease prevalence in population
            * Prior knowledge of the shape of the epidemic curve.
        #. Lack of testing makes this necessary b/c no knowledge of asymptomatic cases.
        #. See [@jacobsen16], only single differential equation needed
            * Optimized using Maximum Likelihood Estimation
            * Use negative log-likelihood b/c it is numerically stable. 
            * Use quasi newton's algorithm

        #. Assumptions 
            * Each individual has number of neighbors. Drawn from degree distribution
            * Three types. (S)usceptible, (I)nfective, (R)emoved
            * Disease spread occurs over network of contacts
            * Each infected individual
                + recovers or dies
                + Or is restricted from contacting network
        #. Once infected, individual has infections period that has exponential dist.
        #. People who are ill remain infectious and a partial count of new illnesses is observed over time
            * Negligible chance of misdiagnosis.
        #. Estimating Transmission Rates.
        #. Estimating dropout and recovery rates
    #) Geographic Modeling Methods
        #. Estimating Hospital Census over Time
            * 1st statewide model produces time series estimates of cases across state
            * 2nd results are translated into estimated ICU and hospitalizations
                + Estimate case onset time series for each age group based on age stratification in each geographic area modeled.
                + Estimate number of cases that will need hospitalization using age/risk factors
                + Use probability distributions for time from illness to onset of hospitalization   
    #) Description of Data
        #. Demographic Data
            * Downloaded from [US Census Bureau 5-year American Community Survey](https://data.census.gov/cedsci/table?q=dp&tid=ACSDP1Y2018.DP02)
            * Got Hospital market share data (trade secret) from Ohio Hospital Association
        #. Definition of Hospital Catchment Areas.
            * Got Ohio county boundary data from U.S. Census Cartographic Boundary Files.
            * Linked with Hospital market share data
            * Only included areas with ICUs, exclude hospice, long-term care facilities.
            * Defined :
                + Used location of all hospitals in Ohio to generate a Voronoi diagram.
                    - Include neighboring states where applicable.
                    - 205 areas generated
                + Voronoi polygons overlaid with ZIP codes
                + Used Hospital market share file. In metro areas, combined polygons into single metro area
                + Generated 96 Hospital Catchment Areas 
#. Discussion
    a) Comparison with other approaches.
        #. Many use susceptible-infectious-recovered (SIR) framework
            * I=infectious, which requires knowledge of both symptomatic and asymptomatic
                + Info currently unavailable.

#. Appendix A
    a) Detailed Desciption of Statewide Model Development
    #) Network Dynamics Assumptions
        #. Spread occurs over a network of contacts at fixed rate of $\beta > 0$
        #. Infected individual may recover at rate of $\gamma > 0$
        #. Voluntary quarantine rate $\delta > 0$
        #. Infected individuals stay infected for random amount of time per exponential dist
        #. There is a negligible chance of misdiagnosis.


#. Appendix B













            
