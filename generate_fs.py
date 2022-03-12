# -*- coding: utf-8 -*-

"""
===============================================
Financial Statements Generator using XBRL
Meng-Chieh, Liu
2022 March 12th 13:46
===============================================
"""

# Download the compiled XBRL file set first
# https://mops.twse.com.tw/mops/web/t203sb02


import pandas as pd
import glob
from lxml import etree

# the input numbers can be either numeric or string
def get_fs(company_code=2330,financial_statement="income_statement",year=2018, quarter=4, to_csv=False):

    # set subject range according to statement types
    if financial_statement == "income_statement":
        start = "Revenue"
        end = "ProfitLoss"
    if financial_statement == "comprehensive_income_statement":
        start = "Revenue"
        end = "ComprehensiveIncome"
    if financial_statement == "balance_sheet":
        start = "CashAndCashEquivalents"
        end = "EquityAndLiabilities"
    if financial_statement == "statement_of_cash_flow":
        start = "ProfitLossBeforeTax"
        end = "CashAndCashEquivalentsAtEndOfPeriod"

    # get file path
    company_path = glob.glob("tifrs-"+str(year)+"Q"+str(quarter)+"/*"+str(company_code)+"-*.xml")[0]

    # get etree element
    tree = etree.parse(company_path)
    root = tree.getroot()

    # get xml namespace
    ns = root.nsmap["ifrs-full"]

    # preliminary settings
    subject_dict = {}
    control = False
    count=0

    for i in root:

        # turn on control when start subject is met
        if i.tag == '{'+ ns +'}' + start:
            if financial_statement == "statement_of_cash_flow":
                if count == 2:
                    control = True
                count += 1
            else:
                control = True

        # only run when control is on
        if control:

            # capture subject name from whole tag
            subject = i.tag.split("}")[1]

            # only retain first two value of certain subject (meaning two years)
            try:
                if len(subject_dict[subject]) ==2 :
                    continue
            except:
                pass

            # get subject value
            value = i.text

            # store subject name and value in dictionary
            try:
                subject_dict[subject].append(value)
                if subject == end:
                    break
            except:
                subject_dict[subject] = [value]
    
    # transfer dictionary into dataframe
    df = pd.DataFrame()
    for subject in subject_dict:
        df[subject] = subject_dict[subject]

    # rotate dataframe and rename columns by years
    df = df.T.rename(columns={0: str(year)+" Q"+str(quarter),1: str(year-1)+" Q"+str(quarter)})

    # store csv file if True
    if to_csv:
        df.to_csv(str(company_code)+'-'+str(year)+'Q'+str(quarter)+'-'+financial_statement+'.csv', encoding="utf-8")

    return df


if __name__ == '__main__':
    
    # example: TSMC(2330) 2018Q4 & 2017Q4 Income Statements
    df = get_fs(company_code=2330,financial_statement="income_statement",year=2018, quarter=4, to_csv=True)
    print(df)