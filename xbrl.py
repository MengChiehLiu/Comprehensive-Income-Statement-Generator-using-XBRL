# -*- coding: utf-8 -*-
"""
Year 2018 Income Statement Generator using XBRL
Meng-Chieh, Liu
2022 March 11th 22:08
"""

# Download the compiled XBRL file set first
# https://mops.twse.com.tw/mops/web/t203sb02

import xml.etree.ElementTree as ET
import pandas as pd
import glob

# create Income Statement Items list and dict
IS_items = ["Revenue","OperatingExpense","ProfitLossFromOperatingActivities","OtherRevenue","OtherGainsLosses","FinanceCosts",
        "ProfitLossBeforeTax","IncomeTaxExpenseContinuingOperations","ProfitLossFromContinuingOperations","ProfitLoss","OtherComprehensiveIncomeBeforeTaxGainsLossesOnRemeasurementsOfDefinedBenefitPlans",
        "IncomeTaxRelatingToComponentsOfOtherComprehensiveIncomeThatWillNotBeReclassifiedToProfitOrLoss","OtherComprehensiveIncomeThatWillNotBeReclassifiedToProfitOrLossNetOfTax","OtherComprehensiveIncomeBeforeTaxExchangeDifferencesOnTranslation",
        "IncomeTaxRelatingToComponentsOfOtherComprehensiveIncomeThatWillBeReclassifiedToProfitOrLoss","OtherComprehensiveIncomeThatWillBeReclassifiedToProfitOrLossNetOfTax",
        "OtherComprehensiveIncome","ComprehensiveIncome"]
IS_items_dict = {}
for item in IS_items:
    IS_items_dict[item]=[]

# select every file from folder
company_path_list = glob.glob(glob.escape("tifrs-2018Q4") + "/*.xml")
company_list =[]
count=1
max=len(company_path_list)

for company_path in company_path_list:

    # Print Process
    print('\rProcess: ' +"%d/%d finished." %(count,max), end=" ")
    count +=1

    # (Optional)Retain only 4 code company
    company_code = company_path.split("-")[6]
    if len(company_code) != 4:
        continue

    # append company_code and IS_items to list in IS_items_dict according to key
    try:
        company_list.append("\t"+company_code)  # add tab to show leading 0 in exel
        tree = ET.parse(company_path)
        root = tree.getroot()
        
        for item in IS_items_dict:
            try:
                value = root.findall('{http://xbrl.ifrs.org/taxonomy/2017-03-09/ifrs-full}'+item)[0].text
                IS_items_dict[item].append(value)
            except:
                IS_items_dict[item].append(0) # if value not available append 0
    except:
        pass

# transfer list into DataFrame
XBRL = pd.DataFrame()
XBRL["company_code"] = company_list
for item in IS_items:
    XBRL[item] = IS_items_dict[item]

# set company_code as index
XBRL = XBRL.set_index("company_code").sort_index()

# rotate the table
XBRL = XBRL.T

# download csv
XBRL.to_csv("2018_all_comprehensive_income_statement.csv")