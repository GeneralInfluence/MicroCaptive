# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:16:06 2017

@author: ameetrawtani
"""

'''
Client takes the $1M profit distribution.
39.6% Federal tax bracket, 5.75% bracket for Virginia, 3.8% Obamacare tax will be applied. 
Accordingly the net distribution will be $520,000 assuming a combined rate of 48%. 

This sum will be invested. The portfolio will earn at a 5.6% net after tax, after expense rate. 
(50% Muni Bonds earning 3% tax free interest at the federal level plus 
1% unrealized capital appreciation, and paying 5% tax at the state level; 
50% invested in Blue Chip Stocks paying a 3% dividend and 
experiencing unrealized capital appreciation of 5% annually). 

Investments are made annually for 10 years in the same amount.
 
After 10 years, the owner takes distributions. 
The basis is NOT taxed. 

Capital Gains will be taxed at 20%. Distributions will be taken evenly over 10 years.


Goal is to get output, and be able to chart/viz them. Means you should be able 
to generate data to chart for each year.

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline

class scenario_one(object):
    def __init__(self, initial_amount, muni_roi = 1/100, equity_roi = 5/100, muni_int = 3/100, equity_div = 3/100, proportion = 50):
        """
        Scenario One calculates returns with assumptions about investments made,
        taxes, and distributions.
    
        For each year, you know how many years are left for appreciation before distribution.
        
        Proportion is the proportion of the portfolio dedicated to Munis.
        So Equity Investments are 1-proportion/100
        """
        self.initial_amount = initial_amount
        self.muni_roi = muni_roi
        self.equity_roi = equity_roi
        self.muni_int = muni_int
        self.equity_div = equity_div
        self.fed_tax = 39.6/100
        self.state_tax = 5.75/100
        self.aca_tax = 3.8/100
        self.net_init_amount = round(self.initial_amount * (1 - (self.fed_tax + self.state_tax + self.aca_tax)),2)
        self.muni_amount = round(self.net_init_amount*(proportion/100),2)
        self.equity_amount = round(self.net_init_amount*(1-proportion/100),2)
        
        
    def investment_calc(self, investment):
        """
        Calculate the returns in a year, municipal and equity.
        
        Investment is a list with the muni and equity amounts to invest passed
        [self.muni_amount, self.equity_amount].
        
        The principal, muni_amount, appreciates at 1% per annum, untaxed.
        The interest earned, at 3% per annum, is only taxed at state income levels.
        This is automatically reinvested into munis.
        
        So each year, you have two buckets - the principal, and the interest earned, to track.
        
        For equities, we are tracking the portfolio, appreciating at 5% per annum,
        and dividends at 3% per annum.
        
        Assume that the tax rate is based on the sum of interest and dividend income for that year.
        
        """
        #muni basis each year is the muni_amount + all prior year's interest
        self.muni_appreciated = round(investment[0] * (1+self.muni_roi),2)
        self.equity_appreciated = round(investment[1] * (1+self.equity_roi),2)
        
        #Interest and Dividends, pretax
        self.pretax_interest = round(investment[0]*self.muni_int,2)
        self.pretax_dividends = round(investment[1]*self.equity_div,2)
        
        #State Tax Schedule
        if self.pretax_dividends+self.pretax_interest <= 3000:
            self.muni_int_earned = round(self.pretax_interest*(1-2/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-(20+3.8+2)/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 3000) & (self.pretax_dividends+self.pretax_interest <= 5000):
            self.muni_int_earned = round(self.pretax_interest*(1-3/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-(20+3.8+3)/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 5000) & (self.pretax_dividends+self.pretax_interest <= 17000):
            self.muni_int_earned = round(self.pretax_interest*(1-5/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-(20+3.8+5)/100),2)
        else:
            self.muni_int_earned = round(self.pretax_interest*(1-5.75/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-(20+3.8+5.75)/100),2)
        return (self.muni_appreciated, self.muni_int_earned, self.equity_appreciated, self.equity_div_earned)
    
    
        
    
    def total_returns(self, years_inv = 10, years_dist = 10):
        #first calculate what your returns are over the investment only period.
        """
        Calculate investment returns over ten years, and then distributions
        over ten years.
        
        Investments continue to compound as distributions are taken.
        
        The ending distribution amount should clear the investment amounts.
        
        Dividends and interest are not re-taxed.
        
        Cap gains are taxed at 20% + 3.8% ACA tax + 5.75% VA state tax rate.
        """
        
        muni_bases = []
        muni_ending = []
        muni_cap_appr = []
        muni_interest = []
        equity_bases = []
        equity_ending = []
        equity_cap_appr = []
        equity_div = []
        inv_year = []
        for start_year in range(0, years_inv):
            if start_year == 0:
                ending_muni, interest, ending_equity, dividends = self.investment_calc([self.muni_amount,self.equity_amount])
                #munis
                muni_bases.append(self.muni_amount)
                muni_ending.append(ending_muni)
                muni_cap_appr.append(ending_muni - self.muni_amount)
                muni_interest.append(interest)
                #equities
                equity_bases.append(self.equity_amount)
                equity_ending.append(ending_equity)
                equity_cap_appr.append(ending_equity-self.equity_amount)
                equity_div.append(dividends)
                inv_year.append(start_year)
            else:
                #compounding the ending amount from the prior year plus the interest earned in the last year
                ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_ending[start_year-1]+muni_interest[start_year-1]+self.muni_amount,equity_ending[start_year-1]+ equity_div[start_year-1]+self.equity_amount])
                muni_bases.append(self.muni_amount*(start_year+1) + sum(muni_interest.copy()))
                muni_ending.append(ending_muni)
                muni_cap_appr.append(ending_muni - muni_bases.copy()[start_year])
                muni_interest.append(interest)
                #equities
                equity_bases.append(self.equity_amount*(start_year+1) + sum(equity_div.copy()))
                equity_ending.append(ending_equity)
                equity_cap_appr.append(ending_equity-equity_bases.copy()[start_year])
                equity_div.append(dividends)
                inv_year.append(start_year)
                
        #Portfolio at start of year 10, right before distributions
        div_int_year10 = muni_interest[9]+ equity_div[9]
        portfolio_year10 = muni_ending[9]+equity_ending[9]+div_int_year10
        distribution = portfolio_year10/8
        
        
        #bases needs to show the bases for each year.
        #bases would be 260K in year 0, 260K + 260K + last year's int in year 1, 
        self.total_df = pd.DataFrame([inv_year,muni_bases, muni_ending, muni_cap_appr, muni_interest, equity_bases, equity_ending, equity_cap_appr, equity_div]).T.rename(columns = {0: 'Starting Year', 1:'muni_cost', 2:'muni_end_amt', 3: 'muni_capgain', 4:'net_int', 5: 'equity_cost', 6: 'equity_end_amt', 7: 'equity_cap_gain', 8:'net_div'}).set_index('Starting Year')
        return self.total_df
        #return (muni_bases, muni_ending, muni_cap_appr, muni_interest)
        
    def distributions(self, port_df, years_dist = 10):
        """
        Calculating overall distribution necessary to exhaust portfolio.
        
        Distribution will exhaust equity portfolio first (b/c traditionally
        fixed income is held as one gets older). It will also exhaust divs
        and interest each year.
        
        There will be a distribution each year, and then a final one at the
        end of year 20, coming out to 11 distributions.
        
        The final distribution should be equal to interest and the remaining
        balance of the municipal bond portfolio if the equity is fully exhausted
        before then.
        """
        capgain_adjuster = 1-(20+3.8+5.75)/100
        #Starting dist
        distribution = (port_df.copy()['equity_end_amt'].ix[9]+port_df.copy()['muni_end_amt'].ix[9]+port_df.copy()['net_int'].ix[9]+port_df.copy()['net_div'].ix[9])/years_dist
        
        tracker = 0
        
        while tracker ==0:
            temp_muni_end = []
            temp_interest = [port_df.copy()['net_int'].ix[9]]
            temp_eq_end = []
            temp_div = [port_df.copy()['net_div'].ix[9]]
            temp_muni_start = [port_df.copy()['muni_end_amt'].ix[9]]
            temp_eq_start = [port_df.copy()['equity_end_amt'].ix[9]]
            temp_muni_bases = [port_df.copy()['muni_cost'].ix[9]]
            temp_eq_bases = [port_df.copy()['equity_cost'].ix[9]]
            dists = []
            
                
            #counter is the start of the year. So year 10 in count is when everything should be done at start of year.
            for dist_year in range(0, years_dist):
                #Calculating the dividends and interest avail at start of dist year.
                div_int_year_start = temp_interest[dist_year]+temp_div[dist_year]
                portfolio_start = div_int_year_start + temp_eq_start[dist_year]+temp_muni_start[dist_year]
                #Amount to be taken out of portfolios.
                nondivint_amount = distribution - div_int_year_start
#                print (nondivint_amount)
#                print ("adj for cap gain", nondivint_amount/capgain_adjuster)
                eq_after_dist = 0
                remain_dist_needed = 0
                muni_after = 0
                
                #Exhaust equity first
                if temp_eq_start[dist_year]>0:
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_eq_start[dist_year]-temp_eq_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount/capgain_adjuster
                        eq_base = temp_eq_bases[dist_year]
                        temp_eq_bases.append(eq_base)
                        
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])> 0) & ((temp_eq_start[dist_year]-temp_eq_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_eq_start[dist_year]-temp_eq_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        
                        #this allows eq after dist to go negative. can't allow.
                        eq_after_dist = temp_eq_start[dist_year]-dist_from_gains-remain_dist_needed
                        eq_base = eq_after_dist
                        temp_eq_bases.append(eq_base)
                        remain_dist_needed = 0
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])<= 0) & (temp_eq_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount
                        temp_eq_bases.append(eq_after_dist)
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])<= 0) & (temp_eq_start[dist_year] < nondivint_amount):
                        #exhaust the equity portfolio.
                        eq_after_dist = 0
                        remain_dist_needed = nonintdiv_amount - temp_eq_start[dist_year]
                        temp_eq_bases.append(eq_after_dist)
                
                #goal of this is to exhaust the munis AFTER equities fully distributed.
            
                #first check if need to distribute a remaining amount after distributing equities and still needing to distribute for the year.
                if remain_dist_needed > 0 & (temp_muni_start[dist_year] > 0):
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) >= remain_dist_needed/capgain_adjuster:
                        muni_after = temp_muni_start[dist_year] - remain_dist_needed/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                    #if cap gains < remaining amount to dist
                    elif (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < remain_dist_needed/capgain_adjuster:
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = remain_dist_needed-net_dist_from_gains
                        muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                        temp_muni_bases.append(muni_after)
                        
                #If equities fully distributed and remain_dist_needed = 0
                if (temp_muni_start[dist_year] > 0) & (remain_dist_needed ==0):
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                        
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])> 0) & ((temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                        temp_muni_bases.append(muni_after)
                        remain_dist_needed = 0
                        
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])<= 0) & (temp_muni_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount
                        temp_muni_bases.append(muni_after)
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])<= 0) & (temp_muni_start[dist_year] < nondivint_amount):
                        #exhaust the muni portfolio.
                        muni_after = 0
                        temp_muni_bases.append(muni_after)
                            
                #distributions taken.
                
                
                #now compound the muni and equity after dists
                ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_after, eq_after_dist])
                #need to check the 
                temp_muni_end.append(ending_muni)
                #muni start for next year is this year's ending value
                temp_muni_start.append(ending_muni)
                temp_interest.append(interest)
                temp_eq_end.append(ending_equity)
                #equity start for next year is this year's ending value
                temp_eq_start.append(ending_equity)
                temp_div.append(dividends)
                
            #distribution+=1
            inv_year = list(range(10,21))
            self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
            tracker += 1
            
            #if dist > ending amount, and continues to increase, want to stop!!!
            
#            if round(distribution - temp_muni_start[-1] - temp_interest[-1],-3) > 0:
#                distribution -= 100
#            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],-3) < 0:
#                distribution += 100
#            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],-3) == 0:
#            #if round(distribution - temp_muni_start[-1] - temp_interest[-1],0) == 0:
#                inv_year = list(range(10,21))
#                print ("Distribution Amount per year:", distribution)
#                print ("Ending Amount", temp_muni_start[-1] - temp_interest[-1])
#                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_muni_end-temp_muni_bases, temp_muni_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_eq_end-temp_eq_bases, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4: 'muni_capgain', 5:'net_int', 6: 'eq_start', 7: 'equity_cost', 8: 'equity_end_amt', 9: 'equity_cap_gain', 10:'net_div'}).set_index('Starting Year')
#                break
        return self.dist_df

   
        
        
def muni_returns(muni_amount, start_year, muni_roi = 1/100, muni_int = 3/100):
    """
    Calculate the returns in a year.
    
    The principle, muni_amount, appreciates at 1% per annum, untaxed.
    The interest earned, at 3% per annum, is only taxed at state income levels.
    This is automatically reinvested into munis.
    
    So each year, you have two buckets - the principle, and the interest earned, to track.
    """
    muni_basis = muni_amount
    muni_appreciated = muni_amount * ((1+muni_roi)**(10-start_year))
    muni_cap_appreciation = muni_appreciated - muni_amount
    muni_int_earned = muni_amount*muni_int*(1-5/100)
    return (muni_appreciated, muni_basis, muni_cap_appreciation, muni_int_earned)
    
    


    
def principle_rate(principle,rate=3,tax=0):
  total = principle * (1 + rate /100)
  taxes_paid = (total-principle) *tax/100
  return principle, taxes_paid

#def dividends(principle,rate=3,tax=0):
  

def scenario1(profit,fed_tax,state_tax,aca_tax,roi=5.6,years=10):
  # We will examine a top tax bracket client in Virginia with and without an 831(b) Captive.We will look at the after tax results on a hypothetical $1M, K-1 distribution from an S-Corp (very common for Brian’s clients) versus using that same sum to pay premiums to their Captive.
  # total_tax = fed_tax + state_tax + aca_tax # ??? assuming a combined rate of 48%
  # net_distribution = profit * (1 - total_tax/100)

  fed_lvl = profit/2
  cap_app = profit/2

  # Federal First
  for y in range(years):
    fed_lvl, state_taxes_paid = principle_rate(fed_lvl,rate=3,tax=5)
    fed_lvl, state_taxes_paid = principle_rate(fed_lvl, rate=3, tax=5)


  # money = 0
  # for y in range(years):
  #   money += net_distribution * (1+roi/100)
  return money

#def scenario2()