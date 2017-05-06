# MicroCaptive
Visualizing Captive Insurance

The Python Script has two scenarios:

1) Scenario 1, where distributions from a K-1 type of entity (LLP, etc) are invested based on certain assumptions.

2) Scenario 2, where an 831(b) captive insurer gets the distributions from the K-1 entity paid as premiums, which are then invested.

## Distributions Assumptions

As the distributions calculations are more complex, here are the assumptions we used:

1) Distributions come out of the equity portfolio first. Reason: As retirees age, usually they are advised to rely more on fixed income. So we are funding distributions out of the equity portfolio first.
2) Once the equity portfolio is fully sold, distributions come out of the bond portfolio.
3) Distribution amounts are distributed at the start of each year and then once at the end of year 20 to exhaust the portfolio, totaling 11 distributions. 
  (Year 1 has an index of 0, and Year 20 has an index of 19. The end of Year 20 is the start of Year 21, marked with index 20 in the DataFrame.)
4) Distributions include the amount needed to pay capital gains taxes on amounts sold.
5) Dividends and Interest, net of tax, are included in the distributions.
6) Hence: Dividends + Interest + Capital Gains to be Paid + Net Capital Sold = Distribution.
7) Related, After Tax Income is assumed to be: Dividends + Interest + Net Capital Sold

Note: Net Capital Sold has to be calculated from the DataFrame, like this: Distribution - Capital Gains to be Paid - Dividends - Interest (script can be altered to directly provide it).

## Running the Script

The script can be run directly in an interpreter, and will run the two client scenarios and save dataframes of the data for visualization purposes to the local directory (later version can save to a user-defined path).

If you want to run the script in Spyder, Atom or something else and not automatically run the scenarios, I recommend you comment out the last lines of script.

In that case, to get the information you want for a scenario, do the below when in a IDE:

0) Import the scenario classes:
from va_scenariocalculator import scenario_one, scenario_two
1) Create a client (if you want to toggle the initial amount, then do initial_amount = your_number):
i.e. clientx = scenario_one()
2) Call the total_returns() method:
i.e. clientx.total_returns().
3) Call the distributions method (recommend that you set a hypothesis distribution, like 750900 for scenario 1, and 1251000 for scenario 2, for faster results, which also is what you would do in Excel with Goal Seek):
i.e. clientx.distributions()

# Methods
## Total_returns()

This method returns a DataFrame of the portfolio investments from year 1 to 10.

## Distributions()

This returns two dataframes:
1) A dataframe tracking the portfolio's muni and equity components over the 10 year distribution period.
2) A dataframe showing the distribution per year (which includes the amount needed to pay capgains taxes), the proportion of the distribution that is principal from the muni or equity portfolio, and the capgains taxes paid that year.

**After Tax Income each year will be the difference of distributions and capgains paid for that year.**



