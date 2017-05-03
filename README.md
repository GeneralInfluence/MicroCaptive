# MicroCaptive
Visualizing Captive Insurance

The Python Script has two scenarios:

1) Scenario 1, where distributions from a K-1 type of entity (LLP, etc) are invested based on certain assumptions.

2) Scenario 2, where an 831(b) captive insurer gets the distributions from the K-1 entity paid as premiums, which are then invested.

To properly use the script for a scenario:

1) Create a client (if you want to toggle the initial amount, then do initial_amount = your_number):
i.e. clientx = scenario_one()
2) Call the total_returns() method:
i.e. clientx.total_returns().
3) Call the distributions method (recommend that you set a hypothesis distribution, like 750900):
i.e. clientx.distributions()

<b>Methods</b>
# Total_returns()

This method returns a DataFrame of the portfolio investments from year 1 to 10.

# Distributions()

This returns two dataframes:
1) A dataframe tracking the portfolio's muni and equity components over the 10 year distribution period.
2) A dataframe showing the distribution per year (which includes the amount needed to pay capgains taxes), the proportion of the distribution that is principal from the muni or equity portfolio, and the capgains taxes paid that year.
**After Tax Income each year will be the difference of distributions and capgains paid for that year.**



