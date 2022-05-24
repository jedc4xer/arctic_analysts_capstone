# arctic_analysts_capstone
Dev10 Capstone Project Repository

Introduction:

Analysis Summary

    Owning a home is a long-term goal for many Americans, and the trends of recent years have<br>
    caused many to question their abilitity for purchase a home as prices have increased rapidly.<br>
    In this analysis, we looked at affordability specifically in New Jersey by at the county level.<br>
    We will use current house prices, the average mortgage interest rate, and forecasted Median Income<br>
    to classify counties as affordable or not affordable.

    The factors that we considered for this analysis were:

    - Median Income
    - New Housing Permits
    - Average Mortgage Interest Rate
    - Median House Prices
    
    We were able to get current data for all of our variables except for Median Income, which was gathered<br>
    from the US Census ACS and was last updated in 2019. In order to fill in the gaps, we will be using a <br>
    time-series model on the U.S. Income Data to get a forecast of current income levels.

    We are defining home affordability as when the monthly mortgage payment including the average property tax<br>
    is less than or equal to 25% of a household's monthly median income given a 20% down-payment.

    A county will be considered affordable if a household making the median income will be able to <br>
    afford a home that is a median priced home in that county.
    
How to run the script:
    
    ```
    cd arctic_analysts_capstone/code/dashboard
    python dashboard_control.py
    ```
        
Repository Layout:

    - Directories
        - Project Specifications/
            - NapkinDrawings/
                - Napkin Drawings
            - Project Specification Files
        - code/
            - Azure_SQL/
                - Database Creation Code
            - dashboard/
                - code files
            - ml_models/
                - Jupyter Notebooks with model testing
