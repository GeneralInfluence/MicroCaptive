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
    def __init__(self, initial_amount=1000000, muni_roi = 1/100, equity_roi = 5/100, muni_int = 3/100, equity_div = 3/100, proportion = 50):
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
                
       
        #bases needs to show the bases for each year.
        #bases would be 260K in year 0, 260K + 260K + last year's int in year 1, 
        self.total_df = pd.DataFrame([inv_year,muni_bases, muni_ending, muni_cap_appr, muni_interest, equity_bases, equity_ending, equity_cap_appr, equity_div]).T.rename(columns = {0: 'Starting Year', 1:'muni_cost', 2:'muni_end_amt', 3: 'muni_capgain', 4:'net_int', 5: 'equity_cost', 6: 'equity_end_amt', 7: 'equity_cap_gain', 8:'net_div'}).set_index('Starting Year')
        
        return self.total_df
        
        #return (muni_bases, muni_ending, muni_cap_appr, muni_interest)
        
    def distributions(self, years_dist = 10, distribution = 0):
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
        
        #Starting dist
        if distribution == 0:
            distribution = (self.total_df.copy()['equity_end_amt'].ix[9]+self.total_df.copy()['muni_end_amt'].ix[9]+self.total_df.copy()['net_int'].ix[9]+self.total_df.copy()['net_div'].ix[9])/(years_dist-2)
        
        
        
        distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -5, 10000)
        while round(distribution - self.dist_df.muni_start[20]-self.dist_df.net_int[20], 0)!=0:
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -4, 1000)
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -3, 100)
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -2, 10)
            distribution, self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -1, 1)
            distribution,   self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, 0, .1)
            print ("Final iteration done. Goal found.")

        return (self.dist_df, self.dist_info)

        
        
        #one big Goal Seek loop.
        #could numpy make this faster?
        #dynamic programming?
#        while tracker <20000:
#            temp_muni_end = []
#            temp_interest = [self.total_df.copy()['net_int'].ix[9]]
#            temp_eq_end = []
#            temp_div = [self.total_df.copy()['net_div'].ix[9]]
#            temp_muni_start = [self.total_df.copy()['muni_end_amt'].ix[9]]
#            temp_eq_start = [self.total_df.copy()['equity_end_amt'].ix[9]]
#            temp_muni_bases = [self.total_df.copy()['muni_cost'].ix[9]]
#            temp_eq_bases = [self.total_df.copy()['equity_cost'].ix[9]]
#            dists = []
#            tax_list = []
#            dist_nondiv = []
#                
#            #counter is the start of the year. So year 10 in count is when everything should be done at start of year.
#            for dist_year in range(0, years_dist):
#                #Calculating the dividends and interest avail at start of dist year.
#                div_int_year_start = temp_interest[dist_year]+temp_div[dist_year]
#                portfolio_start = div_int_year_start + temp_eq_start[dist_year]+temp_muni_start[dist_year]
#                #Amount to be taken out of portfolios.
#                nondivint_amount = distribution - div_int_year_start
##                print (nondivint_amount)
##                print ("adj for cap gain", nondivint_amount/capgain_adjuster)
#                eq_after_dist = 0
#                remain_dist_needed = 0
#                muni_after = temp_muni_start[-1]
#                dists.append(distribution)
#                dist_nondiv.append(nondivint_amount)
#                taxes = 0
#                
#                #Exhaust equity first
#                if temp_eq_start[dist_year]>0:
#                    #Check if nondivint_amount exhausts cap gains.
#                    if (temp_eq_start[dist_year]-temp_eq_bases[dist_year])>= nondivint_amount/capgain_adjuster:
#                        #Take out from the starting amount the dist.
#                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount/capgain_adjuster
#                        eq_base = temp_eq_bases[dist_year]
#                        temp_eq_bases.append(eq_base)
#                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
#                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
#                    #Checking if nondivint_amount > cap gains.
#                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])> 0) & ((temp_eq_start[dist_year]-temp_eq_bases[dist_year]) < nondivint_amount/capgain_adjuster):
#                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
#                        dist_from_gains = temp_eq_start[dist_year]-temp_eq_bases[dist_year]
#                        #net gains after tax
#                        net_dist_from_gains = dist_from_gains*capgain_adjuster
#                        taxes+=dist_from_gains-net_dist_from_gains
#                        remain_dist_needed = nondivint_amount - net_dist_from_gains
#                        
#                        
#                        
#                        if temp_eq_start[dist_year]-dist_from_gains >= remain_dist_needed:
#                            eq_after_dist = temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed
#                            remain_dist_needed = 0
#                            temp_muni_bases.append(temp_muni_bases.copy()[-1])
#                        else:
#                            eq_after_dist = 0
#                            remain_dist_needed = abs(temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed)
#                        eq_base = eq_after_dist
#                        temp_eq_bases.append(eq_base)
#                        
#                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] >= nondivint_amount):
#                        #No cap gains to take out - just base.
#                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount
#                        temp_eq_bases.append(eq_after_dist)
#                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
#                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] < nondivint_amount):
#                        #exhaust the equity portfolio.
#                        eq_after_dist = 0
#                        remain_dist_needed = nondivint_amount - temp_eq_start[dist_year]
#                        temp_eq_bases.append(eq_after_dist)
#                
#                #goal of this is to exhaust the munis AFTER equities fully distributed.
#            
#                #first check if need to distribute a remaining amount after distributing equities and still needing to distribute for the year.
#                if remain_dist_needed > 0 & (temp_muni_start[dist_year] > 0):
#                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) >= remain_dist_needed/capgain_adjuster:
#                        muni_after = temp_muni_start[dist_year] - remain_dist_needed/capgain_adjuster
#                        muni_base = temp_muni_bases[dist_year]
#                        temp_muni_bases.append(muni_base)
#                        taxes+=remain_dist_needed/capgain_adjuster-remain_dist_needed
#                    #if cap gains < remaining amount to dist
#                    elif (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < remain_dist_needed/capgain_adjuster:
#                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
#                        net_dist_from_gains = dist_from_gains*capgain_adjuster
#                        remain_dist_needed = remain_dist_needed-net_dist_from_gains
#                        muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
#                        temp_muni_bases.append(muni_after)
#                        taxes+=dist_from_gains-net_dist_from_gains
#                        
#                #If equities fully distributed and remain_dist_needed = 0
#                if (temp_eq_start[dist_year] == 0) & (remain_dist_needed ==0):
#                    #Check if nondivint_amount exhausts cap gains.
#                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year])>= nondivint_amount/capgain_adjuster:
#                        #Take out from the starting amount the dist.
#                        muni_after = temp_muni_start[dist_year]-nondivint_amount/capgain_adjuster
#                        muni_base = temp_muni_bases[dist_year]
#                        temp_muni_bases.append(muni_base)
#                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
#                    #Checking if nondivint_amount > cap gains.
#                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])> 0) & ((temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < nondivint_amount/capgain_adjuster):
#                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
#                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
#                        #net gains after tax
#                        net_dist_from_gains = dist_from_gains*capgain_adjuster
#                        remain_dist_needed = nondivint_amount - net_dist_from_gains
#                        if temp_muni_start[dist_year]-dist_from_gains >= remain_dist_needed:
#                            muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
#                            remain_dist_needed = 0
#                            temp_muni_bases.append(muni_after)
#                        else:
#                            muni_after = 0
#                            remain_dist_needed = 0
#                            temp_muni_bases.append(muni_after)
#                        
#                        taxes+=dist_from_gains-net_dist_from_gains
#                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] >= nondivint_amount):
#                        #No cap gains to take out - just base.
#                        muni_after = temp_muni_start[dist_year]-nondivint_amount
#                        temp_muni_bases.append(muni_after)
#                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] < nondivint_amount):
#                        #exhaust the muni portfolio.
#                        muni_after = 0
#                        temp_muni_bases.append(muni_after)
#                            
#                #distributions taken.
#                tax_list.append(taxes)
#                
#                #now compound the muni and equity after dists
#                try:
#                    ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_after, eq_after_dist])
#                except ZeroDivisionError:
#                    ending_muni, interest, ending_equity, dividends= [0,0,0,0]
#                
#                #need to check the 
#                temp_muni_end.append(ending_muni)
#                #muni start for next year is this year's ending value
#                temp_muni_start.append(ending_muni)
#                
#                temp_interest.append(interest)
#                temp_eq_end.append(ending_equity)
#                #equity start for next year is this year's ending value
#                temp_eq_start.append(ending_equity)
#                temp_div.append(dividends)
#                
#            #distribution+=1
#            inv_year = list(range(10,21))
#            dists.append(distribution)
#            nondivint_amount = distribution - temp_interest[-1]-temp_div[-1]
#            dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
#            #net gains after tax
#            net_dist_from_gains = dist_from_gains*capgain_adjuster
#            dist_nondiv.append(nondivint_amount)
#            tax_list.append(dist_from_gains-net_dist_from_gains)
#            tracker+=1
#            #if dist > ending amount, and continues to increase, want to stop!!!
#            #Part of the Goal Seek logic.
#            if round(distribution - temp_muni_start[-1] - temp_interest[-1],1) > 0:
#                distribution -= .01
#                
#                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
#                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
#                
#            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],1) < 0:
#                distribution += .01
#                
#                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
#                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
#                
#            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],1) == 0:
#                #if round(distribution - temp_muni_start[-1] - temp_interest[-1],0) == 0:
##                inv_year = list(range(10,21))
#                print ("Distribution Amount per year:", distribution)
#                print ("Ending Amount:", temp_muni_start[-1] + temp_interest[-1])
#                print ("Loops:", tracker)
#                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
#                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
#                break
#        return (self.dist_df, self.dist_info)

    
    def goal_seek(self, distribution, years_dist, rounder, increment):
        capgain_adjuster = 1-(20)/100
        #converge = False
        tracker = 0
        while tracker <=1000:
            #print (tracker)
            temp_muni_end = []
            temp_interest = [self.total_df.copy()['net_int'].ix[9]]
            temp_eq_end = []
            temp_div = [self.total_df.copy()['net_div'].ix[9]]
            temp_muni_start = [self.total_df.copy()['muni_end_amt'].ix[9]]
            temp_eq_start = [self.total_df.copy()['equity_end_amt'].ix[9]]
            temp_muni_bases = [self.total_df.copy()['muni_cost'].ix[9]]
            temp_eq_bases = [self.total_df.copy()['equity_cost'].ix[9]]
            dists = []
            tax_list = []
            dist_nondiv = []
                
            #counter is the start of the year. So year 10 in count is when everything should be done at start of year.
            for dist_year in range(0, years_dist):
                #Calculating the dividends and interest avail at start of dist year.
                div_int_year_start = temp_interest[dist_year]+temp_div[dist_year]
                
                #Amount to be taken out of portfolios.
                nondivint_amount = distribution - div_int_year_start
#                print (nondivint_amount)
#                print ("adj for cap gain", nondivint_amount/capgain_adjuster)
                eq_after_dist = 0
                remain_dist_needed = 0
                muni_after = temp_muni_start[-1]
                dists.append(distribution)
                dist_nondiv.append(nondivint_amount)
                taxes = 0
                
                #Exhaust equity first
                if temp_eq_start[dist_year]>0:
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_eq_start[dist_year]-temp_eq_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount/capgain_adjuster
                        eq_base = temp_eq_bases[dist_year]
                        temp_eq_bases.append(eq_base)
                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])> 0) & ((temp_eq_start[dist_year]-temp_eq_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_eq_start[dist_year]-temp_eq_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        taxes+=dist_from_gains-net_dist_from_gains
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        
                        
                        
                        if temp_eq_start[dist_year]-dist_from_gains >= remain_dist_needed:
                            eq_after_dist = temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed
                            remain_dist_needed = 0
                            temp_muni_bases.append(temp_muni_bases.copy()[-1])
                        else:
                            eq_after_dist = 0
                            remain_dist_needed = abs(temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed)
                        eq_base = eq_after_dist
                        temp_eq_bases.append(eq_base)
                        
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount
                        temp_eq_bases.append(eq_after_dist)
                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] < nondivint_amount):
                        #exhaust the equity portfolio.
                        eq_after_dist = 0
                        remain_dist_needed = nondivint_amount - temp_eq_start[dist_year]
                        temp_eq_bases.append(eq_after_dist)
                
                #goal of this is to exhaust the munis AFTER equities fully distributed.
            
                #first check if need to distribute a remaining amount after distributing equities and still needing to distribute for the year.
                if remain_dist_needed > 0 & (temp_muni_start[dist_year] > 0):
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) >= remain_dist_needed/capgain_adjuster:
                        muni_after = temp_muni_start[dist_year] - remain_dist_needed/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                        taxes+=remain_dist_needed/capgain_adjuster-remain_dist_needed
                    #if cap gains < remaining amount to dist
                    elif (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < remain_dist_needed/capgain_adjuster:
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = remain_dist_needed-net_dist_from_gains
                        muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                        temp_muni_bases.append(muni_after)
                        taxes+=dist_from_gains-net_dist_from_gains
                        
                #If equities fully distributed and remain_dist_needed = 0
                if (temp_eq_start[dist_year] == 0) & (remain_dist_needed ==0):
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])> 0) & ((temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        if temp_muni_start[dist_year]-dist_from_gains >= remain_dist_needed:
                            muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                            remain_dist_needed = 0
                            temp_muni_bases.append(muni_after)
                        else:
                            muni_after = 0
                            remain_dist_needed = 0
                            temp_muni_bases.append(muni_after)
                        taxes+=dist_from_gains-net_dist_from_gains
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount
                        temp_muni_bases.append(muni_after)
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] < nondivint_amount):
                        #exhaust the muni portfolio.
                        muni_after = 0
                        temp_muni_bases.append(muni_after)
                            
                #distributions taken.
                tax_list.append(taxes)
                
                #now compound the muni and equity after dists
                try:
                    ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_after, eq_after_dist])
                except ZeroDivisionError:
                    ending_muni, interest, ending_equity, dividends= [0,0,0,0]
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
            dists.append(distribution)
            nondivint_amount = distribution - temp_interest[-1]-temp_div[-1]
            dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
            #net gains after tax
            net_dist_from_gains = dist_from_gains*capgain_adjuster
            dist_nondiv.append(nondivint_amount)
            tax_list.append(dist_from_gains-net_dist_from_gains)
            #self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
            #self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
            
            tracker+=1
            #if dist > ending amount, and continues to increase, want to stop!!!
            #Part of the Goal Seek logic.
            if round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) > 0:
                distribution -= increment
                
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) < 0:
                distribution += increment
                
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) == 0:
                #if round(distribution - temp_muni_start[-1] - temp_interest[-1],0) == 0:
#                inv_year = list(range(10,21))
                print ("Distribution Amount per year:", distribution)
                print ("Ending Amount:", temp_muni_start[-1] + temp_interest[-1])
                print ("Loops:", tracker)
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
                #converge = True
                break
            
            #Tracker for if loops do not converge.
            if tracker == 2000:
                print ("Distribution Amount per year:", distribution)
                print ("Ending Amount:", temp_muni_start[-1] + temp_interest[-1])
                print ("Loops:", tracker)
                print ("Try re-running with a different starting distribution.")
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
                break
        return (distribution, self.dist_df, self.dist_info)


class scenario_two(object):
    def __init__(self, initial_amount=950000, reserve_fund = 190000, muni_roi = 1/100, equity_roi = 5/100, muni_int = 3/100, equity_div = 3/100, proportion = 50):
        """
        Scenario Two calculates returns with assumptions about investments made,
        taxes, and distributions.
        
        $1MM in premiums are paid each year, but for simplicity, we assume
        that $950k are the net premiums ($50k in expenses deducted per year.)
        Could make adjustable later if we know if and how expenses vary with
        premiums paid.
        
        Premiums are not taxed. Dividends and Interest are taxed at corporate rates.
        
        For each year, you know how many years are left for appreciation before distribution.
        
        Proportion is the proportion of the portfolio dedicated to Munis.
        So Equity Investments are 1-proportion/100
        """
        self.initial_amount = initial_amount
        self.muni_roi = muni_roi
        self.equity_roi = equity_roi
        self.muni_int = muni_int
        self.equity_div = equity_div
        self.reserve_fund = reserve_fund
        self.muni_yr1 = round((self.initial_amount-self.reserve_fund)*(proportion/100),2)
        self.eq_yr1 = round((self.initial_amount-self.reserve_fund)*(1-proportion/100),2)
        #For years 2-10.
        self.muni_amt = round(self.initial_amount*(proportion/100),2)
        self.equity_amt = round(self.initial_amount*(1-proportion/100),2)
        
    def investment_calc(self, investment):
        """
        Calculate the returns in a year, municipal and equity.
        
        Investment is a list with the muni and equity amounts to invest passed
        [self.muni_amt, self.equity_amt].
        
        The principal, muni_amount, appreciates at 1% per annum, untaxed.
        The interest earned, at 3% per annum, is only taxed at state income levels.
        This is automatically reinvested into munis.
        
        So each year, you have two buckets - the principal, and the interest earned, to track.
        
        For equities, we are tracking the portfolio, appreciating at 5% per annum,
        and dividends at 3% per annum.
        
        Corporate Tax Rate for 831b is here: https://www.irs.gov/pub/irs-pdf/i1120pc.pdf
  
        
        """
        
        
        #muni basis each year is the muni_amount + all prior year's interest
        self.muni_appreciated = round(investment[0] * (1+self.muni_roi),2)
        self.equity_appreciated = round(investment[1] * (1+self.equity_roi),2)
        
        #Interest and Dividends, pretax
        self.pretax_interest = round(investment[0]*self.muni_int,2)
        self.pretax_dividends = round(investment[1]*self.equity_div,2)
        
        muni_percent = self.pretax_interest/(self.pretax_interest+self.pretax_dividends)
        
        #Corp Tax Schedule
        if self.pretax_dividends+self.pretax_interest <= 50000:
            self.muni_int_earned = round(self.pretax_interest*(1-15/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-15/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 50000) & (self.pretax_dividends+self.pretax_interest <= 75000):
            #Will split the amount proportionally.
            self.muni_int_earned = round((self.pretax_interest-(7500*muni_percent))*(1-25/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(7500*(1-muni_percent)))*(1-25/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 75000) & (self.pretax_dividends+self.pretax_interest <= 100000):
            self.muni_int_earned = round((self.pretax_interest-(13750*muni_percent))*(1-34/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(13750*(1-muni_percent)))*(1-34/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 100000) & (self.pretax_dividends+self.pretax_interest <= 335000):
            self.muni_int_earned = round((self.pretax_interest-(22250*muni_percent))*(1-39/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(22250*(1-muni_percent)))*(1-39/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 335000) & (self.pretax_dividends+self.pretax_interest <= 10000000):
            self.muni_int_earned = round((self.pretax_interest-(113900*muni_percent))*(1-34/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(113900*(1-muni_percent)))*(1-34/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 10000000) & (self.pretax_dividends+self.pretax_interest <= 15000000):
            self.muni_int_earned = round((self.pretax_interest-(3400000*muni_percent))*(1-35/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(3400000*(1-muni_percent)))*(1-35/100),2)
        elif (self.pretax_dividends+self.pretax_interest > 15000000) & (self.pretax_dividends+self.pretax_interest <= 18333333):
            self.muni_int_earned = round((self.pretax_interest-(5150000*muni_percent))*(1-38/100),2)
            self.equity_div_earned = round((self.pretax_dividends-(5150000*(1-muni_percent)))*(1-38/100),2)
        
        else:
            self.muni_int_earned = round(self.pretax_interest*(1-35/100),2)
            self.equity_div_earned = round(self.pretax_dividends*(1-35/100),2)
        return (self.muni_appreciated, self.muni_int_earned, self.equity_appreciated, self.equity_div_earned)
    
    
        
    
    def total_returns(self, years_inv = 10):
        #first calculate what your returns are over the investment only period.
        """
        Calculate investment returns over ten years, and then distributions
        over ten years.
        
        Investments continue to compound as distributions are taken.
        
        The ending distribution amount should clear the investment amounts.
        
        Dividends and interest are not re-taxed.
        
        Cap gains are taxed at 20% + 3.8% ACA tax + 5.75% VA state tax rate.
        """
        reserve = []
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
                reserve.append(round(self.reserve_fund*1.01,2))
                ending_muni, interest, ending_equity, dividends = self.investment_calc([self.muni_yr1,self.eq_yr1])
                #munis
                muni_bases.append(self.muni_yr1)
                muni_ending.append(ending_muni)
                muni_cap_appr.append(ending_muni - self.muni_yr1)
                muni_interest.append(interest)
                #equities
                equity_bases.append(self.eq_yr1)
                equity_ending.append(ending_equity)
                equity_cap_appr.append(ending_equity-self.eq_yr1)
                equity_div.append(dividends)
                inv_year.append(start_year)
            else:
                #compounding the ending amount from the prior year plus the interest earned in the last year
                reserve.append(round(reserve.copy()[-1]*1.01,2))
                ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_ending[start_year-1]+muni_interest[start_year-1]+self.muni_amt,equity_ending[start_year-1]+ equity_div[start_year-1]+self.equity_amt])
                muni_bases.append(self.muni_yr1 + self.muni_amt*(start_year) + sum(muni_interest.copy()))
                muni_ending.append(ending_muni)
                muni_cap_appr.append(ending_muni - muni_bases.copy()[start_year])
                muni_interest.append(interest)
                #equities
                equity_bases.append(self.eq_yr1 + self.equity_amt*(start_year) + sum(equity_div.copy()))
                equity_ending.append(ending_equity)
                equity_cap_appr.append(ending_equity-equity_bases.copy()[start_year])
                equity_div.append(dividends)
                inv_year.append(start_year)
                
       
        #bases needs to show the bases for each year.
        #bases would be 260K in year 0, 260K + 260K + last year's int in year 1, 
        self.total_df = pd.DataFrame([inv_year,reserve, muni_bases, muni_ending, muni_cap_appr, muni_interest, equity_bases, equity_ending, equity_cap_appr, equity_div]).T.rename(columns = {0: 'Starting Year', 1:'reserve', 2:'muni_cost', 3:'muni_end_amt', 4: 'muni_capgain', 5:'net_int', 6: 'equity_cost', 7: 'equity_end_amt', 8: 'equity_cap_gain', 9:'net_div'}).set_index('Starting Year')
        return self.total_df
        #return (muni_bases, muni_ending, muni_cap_appr, muni_interest)
        
    def distributions(self, years_dist = 10, distribution = 0):
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
        
        #Starting dist
        if distribution == 0:
            distribution = (self.total_df.copy()['equity_end_amt'].ix[9]+self.total_df.copy()['muni_end_amt'].ix[9]+self.total_df.copy()['net_int'].ix[9]+self.total_df.copy()['net_div'].ix[9])/(years_dist)
        
        
        
        
        #one big Goal Seek loop.
        #could numpy make this faster?
        #dynamic programming?
        distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -5, 10000)
        while round(distribution - self.dist_df.muni_start[20]-self.dist_df.net_int[20], 0)!=0:
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -4, 1000)
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -3, 100)
            distribution,  self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -2, 10)
            distribution, self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, -1, 1)
            distribution,   self.dist_df, self.dist_info = self.goal_seek(distribution, years_dist, 0, .1)
            print ("Final iteration done. Goal found.")

        return (self.dist_df, self.dist_info)
#       

    def goal_seek(self, distribution, years_dist, rounder, increment):
        capgain_adjuster = 1-(20)/100
        #converge = False
        tracker = 0
        while True:
            #print (tracker)
            temp_muni_end = []
            temp_interest = [self.total_df.copy()['net_int'].ix[9]]
            temp_eq_end = []
            temp_div = [self.total_df.copy()['net_div'].ix[9]]
            temp_muni_start = [self.total_df.copy()['muni_end_amt'].ix[9]]
            temp_eq_start = [self.total_df.copy()['equity_end_amt'].ix[9]]
            temp_muni_bases = [self.total_df.copy()['muni_cost'].ix[9]]
            temp_eq_bases = [self.total_df.copy()['equity_cost'].ix[9]]
            dists = []
            tax_list = []
            dist_nondiv = []
                
            #counter is the start of the year. So year 10 in count is when everything should be done at start of year.
            for dist_year in range(0, years_dist):
                #Calculating the dividends and interest avail at start of dist year.
                div_int_year_start = temp_interest[dist_year]+temp_div[dist_year]
                
                #Amount to be taken out of portfolios.
                nondivint_amount = distribution - div_int_year_start
#                print (nondivint_amount)
#                print ("adj for cap gain", nondivint_amount/capgain_adjuster)
                eq_after_dist = 0
                remain_dist_needed = 0
                muni_after = temp_muni_start[-1]
                dists.append(distribution)
                dist_nondiv.append(nondivint_amount)
                taxes = 0
                
                #Exhaust equity first
                if temp_eq_start[dist_year]>0:
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_eq_start[dist_year]-temp_eq_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount/capgain_adjuster
                        eq_base = temp_eq_bases[dist_year]
                        temp_eq_bases.append(eq_base)
                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])> 0) & ((temp_eq_start[dist_year]-temp_eq_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_eq_start[dist_year]-temp_eq_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        taxes+=dist_from_gains-net_dist_from_gains
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        
                        
                        
                        if temp_eq_start[dist_year]-dist_from_gains >= remain_dist_needed:
                            eq_after_dist = temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed
                            remain_dist_needed = 0
                            temp_muni_bases.append(temp_muni_bases.copy()[-1])
                        else:
                            eq_after_dist = 0
                            remain_dist_needed = abs(temp_eq_start[dist_year]-dist_from_gains - remain_dist_needed)
                        eq_base = eq_after_dist
                        temp_eq_bases.append(eq_base)
                        
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        eq_after_dist = temp_eq_start[dist_year]-nondivint_amount
                        temp_eq_bases.append(eq_after_dist)
                        temp_muni_bases.append(temp_muni_bases.copy()[-1])
                    elif ((temp_eq_start[dist_year]-temp_eq_bases[dist_year])== 0) & (temp_eq_start[dist_year] < nondivint_amount):
                        #exhaust the equity portfolio.
                        eq_after_dist = 0
                        remain_dist_needed = nondivint_amount - temp_eq_start[dist_year]
                        temp_eq_bases.append(eq_after_dist)
                
                #goal of this is to exhaust the munis AFTER equities fully distributed.
            
                #first check if need to distribute a remaining amount after distributing equities and still needing to distribute for the year.
                if remain_dist_needed > 0 & (temp_muni_start[dist_year] > 0):
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) >= remain_dist_needed/capgain_adjuster:
                        muni_after = temp_muni_start[dist_year] - remain_dist_needed/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                        taxes+=remain_dist_needed/capgain_adjuster-remain_dist_needed
                    #if cap gains < remaining amount to dist
                    elif (temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < remain_dist_needed/capgain_adjuster:
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = remain_dist_needed-net_dist_from_gains
                        muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                        temp_muni_bases.append(muni_after)
                        taxes+=dist_from_gains-net_dist_from_gains
                        
                #If equities fully distributed and remain_dist_needed = 0
                if (temp_eq_start[dist_year] == 0) & (remain_dist_needed ==0):
                    #Check if nondivint_amount exhausts cap gains.
                    if (temp_muni_start[dist_year]-temp_muni_bases[dist_year])>= nondivint_amount/capgain_adjuster:
                        #Take out from the starting amount the dist.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount/capgain_adjuster
                        muni_base = temp_muni_bases[dist_year]
                        temp_muni_bases.append(muni_base)
                        taxes+=nondivint_amount/capgain_adjuster-nondivint_amount
                    #Checking if nondivint_amount > cap gains.
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])> 0) & ((temp_muni_start[dist_year]-temp_muni_bases[dist_year]) < nondivint_amount/capgain_adjuster):
                        #if cap gains exist but less than amount to distribute, fully exhaust cap gains
                        dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
                        #net gains after tax
                        net_dist_from_gains = dist_from_gains*capgain_adjuster
                        remain_dist_needed = nondivint_amount - net_dist_from_gains
                        if temp_muni_start[dist_year]-dist_from_gains >= remain_dist_needed:
                            muni_after = temp_muni_start[dist_year]-dist_from_gains-remain_dist_needed
                            remain_dist_needed = 0
                            temp_muni_bases.append(muni_after)
                        else:
                            muni_after = 0
                            remain_dist_needed = 0
                            temp_muni_bases.append(muni_after)
                        taxes+=dist_from_gains-net_dist_from_gains
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] >= nondivint_amount):
                        #No cap gains to take out - just base.
                        muni_after = temp_muni_start[dist_year]-nondivint_amount
                        temp_muni_bases.append(muni_after)
                    elif ((temp_muni_start[dist_year]-temp_muni_bases[dist_year])== 0) & (temp_muni_start[dist_year] < nondivint_amount):
                        #exhaust the muni portfolio.
                        muni_after = 0
                        temp_muni_bases.append(muni_after)
                            
                #distributions taken.
                tax_list.append(taxes)
                
                #now compound the muni and equity after dists
                try:
                    ending_muni, interest, ending_equity, dividends = self.investment_calc([muni_after, eq_after_dist])
                except ZeroDivisionError:
                    ending_muni, interest, ending_equity, dividends= [0,0,0,0]
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
            dists.append(distribution)
            nondivint_amount = distribution - temp_interest[-1]-temp_div[-1]
            dist_from_gains = temp_muni_start[dist_year]-temp_muni_bases[dist_year]
            #net gains after tax
            net_dist_from_gains = dist_from_gains*capgain_adjuster
            dist_nondiv.append(nondivint_amount)
            tax_list.append(dist_from_gains-net_dist_from_gains)
            #self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
            #self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
            
            tracker+=1
            #if dist > ending amount, and continues to increase, want to stop!!!
            #Part of the Goal Seek logic.
            if round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) > 0:
                distribution -= increment
                
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) < 0:
                distribution += increment
                
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
            elif round(distribution - temp_muni_start[-1] - temp_interest[-1],rounder) == 0:
                #if round(distribution - temp_muni_start[-1] - temp_interest[-1],0) == 0:
#                inv_year = list(range(10,21))
                print ("Distribution Amount per year:", distribution)
                print ("Ending Amount:", temp_muni_start[-1] + temp_interest[-1])
                print ("Loops:", tracker)
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
                #converge = True
                break
            
            #Tracker for if loops do not converge.
            if tracker == 2000:
                print ("Distribution Amount per year:", distribution)
                print ("Ending Amount:", temp_muni_start[-1] + temp_interest[-1])
                print ("Loops:", tracker)
                print ("Try re-running with a different starting distribution.")
                self.dist_df = pd.DataFrame([inv_year,temp_muni_start, temp_muni_bases, temp_muni_end, temp_interest, temp_eq_start, temp_eq_bases, temp_eq_end, temp_div ]).T.rename(columns = {0: 'Starting Year', 1: 'muni_start', 2:'muni_cost', 3:'muni_end_amt', 4:'net_int', 5: 'eq_start', 6: 'equity_cost', 7: 'equity_end_amt', 8:'net_div'}).set_index('Starting Year')
                self.dist_info = pd.DataFrame([inv_year, dists, dist_nondiv, tax_list]).T.rename(columns = {0:'Starting Year', 1:'dists', 2:'nondivint_dists', 3: 'capgains_paid'}).set_index('Starting Year')
                self.dist_info = self.dist_info.assign(after_tax_income = self.dist_info.dists - self.dist_info.capgains_paid)
                break
        return (distribution, self.dist_df, self.dist_info)

def combine_csvs(df_first10, df_dists):
    df_combined = pd.concat([df_first10, df_dists])
    #Fix Starting Equity Port Value
    df_combined.set_value(0, 'eq_start', df_combined.equity_cost[0])
    df_combined.set_value(0, 'muni_start', df_combined.muni_cost[0])
    for i in range(0,9):
        df_combined.set_value(i+1, 'eq_start', df_combined.equity_end_amt[i])
        df_combined.set_value(i+1, 'muni_start', df_combined.muni_end_amt[i])
    
    #Fix Cap Gain
    for i in range(10, 20):
        df_combined.set_value(i, 'equity_cap_gain', df_combined.eq_start[i]-df_combined.equity_cost[i])
        df_combined.set_value(i, 'muni_capgain', df_combined.muni_start[i]-df_combined.muni_cost[i])
        
    #Fill NA with 0.
    df_combined = df_combined.fillna(0)
    
    #Create Total Assets column
    df_combined = df_combined.assign(total_assets = df_combined.equity_end_amt + df_combined.muni_end_amt)
    
    #Set index to 1 to 21.
    df_combined.set_index([list(range(1,22))], inplace = True)
    df_combined.index.rename('Starting Year', inplace = True)
   
    return df_combined

def after_tax_compare(info1, info2):
    """Combines the distribution info dfs from Scen 1 and 2,
    gets the sum of the After Tax Incomes, and Difference.
    """
    after_tax = pd.merge(info1, info2, left_index = True, right_index = True)
    #Set index to 1 to 21
    after_tax.set_index([list(range(11,22))], inplace = True)
    #Difference in income columnn
    after_tax = after_tax.assign(difference_income = after_tax.after_tax_income_y - after_tax.after_tax_income_x)
    after_tax = after_tax.rename(columns = {'after_tax_income_x': 'income_scen1', 'after_tax_income_y': 'income_scen2'})
    after_tax = after_tax[['income_scen1', 'income_scen2', 'difference_income']]
    after_tax.index.rename('Starting Year', inplace = True)
    return after_tax


#def last_10()

    
   
if __name__ == "__main__":
    #run scenario one
    client1 = scenario_one()
    df_client1_first10 = client1.total_returns()
    df_client1_first10.to_csv('first 10 years portfolio client1.csv')
    df1_dist, df1_info = client1.distributions()
    df1_dist.to_csv('client1_dists.csv')
    df1_info.to_csv('scenario1_distributions.csv')
    df_returns = combine_csvs(df_client1_first10, df1_dist)
    df_returns.to_csv('scenario1_totalreturns_all.csv', index_label = 'Starting Year')
    tot_assets = pd.DataFrame(df_returns[['equity_end_amt', 'muni_end_amt']]) 
    tot_assets.to_csv('scenario1_totalassets.csv', index_label = 'Starting Year')
    
     #run scenario two
    client2 = scenario_two()
    df_client2_first10 = client2.total_returns()
    df_client2_first10.to_csv('first 10 years portfolio client2.csv')
    df2_dist, df2_info = client2.distributions()
    df2_dist.to_csv('client2_dists.csv')
    df2_info.to_csv('scenario2_distributions.csv')
    df_returns2 = combine_csvs(df_client2_first10, df2_dist)
    df_returns2.to_csv('scenario2_totalreturns_all.csv', index_label = 'Starting Year')
    tot_assets2 = pd.DataFrame(df_returns2[['equity_end_amt', 'muni_end_amt']])
    tot_assets2.to_csv('scenario2_totalassets.csv', index_label = 'Starting Year')
    
    
    #Get After Tax Income for two scenarios
    after_tax = after_tax_compare(df1_info, df2_info)
    after_tax.to_csv('scenarios_income.csv', index_label = 'Starting Year')
    