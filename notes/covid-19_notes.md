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

    

