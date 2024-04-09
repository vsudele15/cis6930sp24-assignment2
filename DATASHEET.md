__Datasheet for Assignment 2 Dataset__

**Motivation**
For what purpose was the dataset created?

This dataset was created as part of an assignment (CIS 6930, Spring 2024) to get hands-on experience with data augmentation techniques on incident records extracted from public police department reports. The augmented dataset aims to facilitate further analysis, keeping fairness and bias in mind.

Who created this dataset and on behalf of which entity?

The dataset was created by Vaidehi Sudele of the CIS 6930 course, under the guidance of the University of Florida's Department of Computer & Information Science & Engineering.

**Composition**
What do the instances represent?

Each instance in the dataset represents an augmented record of a police incident, including metadata such as the day of the week, time of day, weather conditions, and incident specifics like nature and EMS status.
How many instances are there in total?

The total number of instances varies depending on the input files processed. Each input PDF containing incident reports contributes to the dataset's size.
What data does each instance consist of?

Day of the Week: Numeric representation (1-7) indicating the day of the week.
Time of Day: Hour of the day (0-24) the incident was reported.
Weather: WMO weather code representing the weather condition at the incident's time and location.
Location Rank: An integer ranking based on the frequency of incidents at the location.
Side of Town: Categorization of the incident's location based on its geographic orientation to the town's center.
Incident Rank: Ranking of the incident's nature based on frequency.
Nature: Direct description of the incident's nature.
EMSSTAT: Boolean indicating if EMS was dispatched.
Is there any missing data?

Data completeness depends on the source PDFs. Missing entries may occur due to extraction errors or incomplete records in the source data.

**COLLECTION PROCESS**

How was the data associated with each instance acquired? Was the data directly observable, reported by subjects, or indirectly inferred/derived from other data (for example, part-of-speech tags, model-based guesses for age or language)? 

The data was indirectly inferred from Norman PD's daily incident summary. There are 8 fields in the data, here is how every field was inferred: a. Day of the week : Day of the week is inferred from DateTime Stamp in the incident Report. Sunday being Day 1 and Saturday being Day 7. b. Time of the Day : Time of the day is inferred from DateTime Stamp in the incident Report and is essentially the hour in the Timestmap. c. Weather : Weather is the WMO code which is fetched from the Weather API. The weather API takes the coordinates of the location and return the WMO code in its response. The coordinates are fetched using Google Maps API which takes the address of the place and returns the coordinates. d. Location Rank : For the Location rank all listed locations sorted and an integer ranking is given based on the frequency of locations with ties preserved. For instance, if there is a three-way tie for the most popular location, each location is ranked 1; the next most popular location is ranked 4 e. Side of town : Is determined based on the cooridnates by calculating the differences between the central and desired coordinates. f. Incident Rank : All of the Natures are sorted. An integer ranking of the frequency of natures is assigned with ties preserved. For instance, if there is a three-way tie for the most popular incident, each incident is ranked 1; the next most popular nature is ranked 4. g. Nature : This field is directly fetched from the report h. EMSSAT : This is a boolean value that is True in two cases. First, if the Incident ORI was EMSSTAT or if the subsequent record or two contain an EMSSTAT at the same time and locaton.

Over what timeframe was the data collected? The data consists from the past 2 months.

How was the data collected? The data was collected using Norman PD's daily incident summary report and then augmenting it by using different functions on it to get the desired fields.

Preprocessing/cleaning/labeling

How was the data preprocessed? The data was preprocessed using Python libraries and python code. Where a csv containing all the pdfs of the daily incidents were stored, the code then fetched every pdf, extracted data from it and preprocessed the data using suitable libraries.
USES

Has the dataset been used for any tasks already? No, it has not been used already

**DISTRIBUTION**

Will the dataset be distributed to third parties outside of the entity (for example, company, institution, organization) on behalf of which the dataset was created? No, it will not be distributed outside

**MAINTENANCE**

Who will be supporting/hosting/maintaining the dataset? Vaidehi Sudele, CS Gradutate student at University of Florida

How can the owner/curator/manager of the dataset be contacted? vsudele@ufl.edu