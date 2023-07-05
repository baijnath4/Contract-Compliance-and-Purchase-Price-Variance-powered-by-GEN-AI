import openai
import pandas as pd

openai.api_key = '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'

def questions(pdf1,i):
    pormptDict = {'Agreement Name':'What is the agreement name,provide only name',
                  'Supplier name':'What is the supplier name',
                  'Start date of the Agreement':'When is the start date and end date of the agreement provide only dates',
                  'Contract id':'what is the contract id',
                  'Payment Terms':'What are the number of days payment terms agreed',
                  'Price per unit':'What are the role wise price per unit not the total value provide in table',
                  'Unit of measure':'What is the unit of measure only'}
    try:
        question = pormptDict[i]
    except:
        question=i
    print("question:-",question)
    prompt = f"{question}\n{pdf1}\n\\n:"
    model = "text-davinci-003"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=500,
        temperature=0,
        n = 1,
        stop=None
    )
    diffs = response.choices[0].text
    return diffs.strip()

def contractandpo(contract,po):
    final_po = pd.merge(contract,po,how='inner',on=['Contract_ID','Line_Item_Desc'])
    final_po = final_po[['PO_ID','Line_Item_Desc','Supplier_x','Payment_Terms_PO','PO_Line_Numb','PO_Quantity','Unit_Of_Measure','Unit_Price_In_Orig_Curr','PO_Spend','Contract_ID','Contract_Payterms','Contracted_Unit_Price']]
    final_po['Contract_Payterms'] = final_po['Contract_Payterms'].astype(int)
    final_po['Contracted_Unit_Price'] = final_po['Contracted_Unit_Price'].astype(int)
    final_po['Payment_Terms_PO'] = final_po['Payment_Terms_PO'].astype(int)
    final_po['Unit_Price_In_Orig_Curr'] = final_po['Unit_Price_In_Orig_Curr'].astype(int)
    final_po['PPV_PO_Contract'] = ((final_po['Unit_Price_In_Orig_Curr'] - final_po['Contracted_Unit_Price'])/final_po['Contracted_Unit_Price'])*100
    final_po['PPV_PO_Contract'] = final_po['PPV_PO_Contract'].astype(int)
    final_po['Payter_Diff_PO_Contract'] = (final_po['Contract_Payterms'] - final_po['Payment_Terms_PO'])
    openai.api_key = "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"
    prompt_s = ['provide the summary of the below data:']
    summary = ''
    summary+= (questions(final_po,prompt_s))    
    return final_po,summary

def contractandinvoice(contract,invoice):
    final_df = pd.merge(contract,invoice,how='inner',on=['Contract_ID','Line_Item_Desc'])
    final_df = final_df[['INVOICE','PO','Contract_ID','Line_Item_Desc','Payment_Terms_PO','Inv_Payterms','Inv_Unit_Price','Contract_Payterms','Contracted_Unit_Price','Inv_Gross_Value','Unit_Price_In_Orig_Curr']]
    final_df['Contract_Payterms'] = final_df['Contract_Payterms'].astype(int)
    final_df['Payment_Terms_PO'] = final_df['Payment_Terms_PO'].astype(int)
    final_df['Inv_Payterms'] = final_df['Inv_Payterms'].astype(int)
    final_df['Inv_Gross_Value'] = final_df['Inv_Gross_Value'].astype(int)
    final_df['Inv_Unit_Price'] = final_df['Inv_Unit_Price'].astype(int)
    final_df['Contracted_Unit_Price'] = final_df['Contracted_Unit_Price'].astype(int)
    final_df['Unit_Price_In_Orig_Curr'] = final_df['Unit_Price_In_Orig_Curr'].astype(int)
    final_df['PPV_Inv_Contract'] = ((final_df['Inv_Unit_Price'] - final_df['Contracted_Unit_Price'])/final_df['Contracted_Unit_Price'])*100
    final_df['PPV_Inv_Contract'] = final_df['PPV_Inv_Contract'].astype(int)
    final_df['Working_Capital_Inv_Contract'] = ((final_df['Contract_Payterms'] - final_df['Inv_Payterms'])*final_df['Inv_Gross_Value'])/365
    final_df = final_df.rename(columns={'INVOICE': 'Doc_Numb', 'PO': 'PO_ID','Unit_Price_In_Orig_Curr':'PO_Unit_Price','Product Description':'Line_Item_Desc'})
    final_df = final_df[['Doc_Numb','Line_Item_Desc','Inv_Payterms','Inv_Unit_Price','PO_ID','Payment_Terms_PO','PO_Unit_Price','Contract_ID','Contract_Payterms','Contracted_Unit_Price','Inv_Gross_Value','PPV_Inv_Contract','Working_Capital_Inv_Contract']]        
    openai.api_key = "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"
    prompt_s = ['provide the summary of the below data:']
    summary = ''
    summary+= (questions(final_df,prompt_s))
    return final_df,summary

def threewaymatch(contract,po,invoice):
    final_df = pd.merge(contract,invoice,how='inner',on=['Contract_ID','Line_Item_Desc'])
    final_df = final_df[['INVOICE','PO','Contract_ID','Line_Item_Desc','Payment_Terms_PO','Inv_Payterms','Inv_Unit_Price','Contract_Payterms','Contracted_Unit_Price','Inv_Gross_Value','Unit_Price_In_Orig_Curr']]
    final_df['Contract_Payterms'] = final_df['Contract_Payterms'].astype(int)
    final_df['Payment_Terms_PO'] = final_df['Payment_Terms_PO'].astype(int)
    final_df['Inv_Payterms'] = final_df['Inv_Payterms'].astype(int)
    final_df['Inv_Gross_Value'] = final_df['Inv_Gross_Value'].astype(int)
    final_df['Inv_Unit_Price'] = final_df['Inv_Unit_Price'].astype(int)
    final_df['Contracted_Unit_Price'] = final_df['Contracted_Unit_Price'].astype(int)
    final_df['Unit_Price_In_Orig_Curr'] = final_df['Unit_Price_In_Orig_Curr'].astype(int)
    final_df['PPV_Inv_Contract'] = ((final_df['Inv_Unit_Price'] - final_df['Contracted_Unit_Price'])/final_df['Contracted_Unit_Price'])*100
    final_df['PPV_Inv_Contract'] = final_df['PPV_Inv_Contract'].astype(int)
    final_df['Working_Capital_Inv_Contract'] = ((final_df['Contract_Payterms'] - final_df['Inv_Payterms'])*final_df['Inv_Gross_Value'])/365
    final_df = final_df.rename(columns={'INVOICE': 'Doc_Numb', 'PO': 'PO_ID','Unit_Price_In_Orig_Curr':'PO_Unit_Price','Product Description':'Line_Item_Desc'})
    final_df = final_df[['Doc_Numb','Line_Item_Desc','Inv_Payterms','Inv_Unit_Price','PO_ID','Payment_Terms_PO','PO_Unit_Price','Contract_ID','Contract_Payterms','Contracted_Unit_Price','Inv_Gross_Value','PPV_Inv_Contract','Working_Capital_Inv_Contract']]        
    final_df = final_df.rename(columns={'INVOICE': 'Doc_Numb', 'PO': 'PO_ID','Unit_Price_In_Orig_Curr':'PO_Unit_Price','Product Description':'Line_Item_Desc','Payment_Terms_PO':'PO_Payterms'})
    final_s = final_df[['Line_Item_Desc','Contracted_Unit_Price','PO_Unit_Price','Inv_Unit_Price','Contract_Payterms','PO_Payterms','Inv_Payterms']]
    openai.api_key = "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"
    prompt_s = ['provide the differences in unit price across contract, PO and Invoice from the table in words and also provide summary of contract,po and Inv_Payterms']
    summary = ''
    summary+= (questions(final_s,prompt_s))
    return final_s,summary

# contractDummy =pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/dummy/C0_1L976.xlsx")
# po = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/upload_3way/PO_updated.xlsx")
# resultDF, reslutSumm=contractandpo(contract=contractDummy,po=po)
# print("result df :--", resultDF)
# print("sum df :--", reslutSumm)


# contractDummy =pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/dummy/C0_1L976.xlsx")
# invoice = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/upload_3way/Invoice data_Updated.xlsx")
# resultDF, reslutSumm=contractandinvoice(contract=contractDummy,invoice=invoice)
# print("result df :--", resultDF)
# print("result df :--", reslutSumm)

# contractDummy =pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/dummy/C0_1L976.xlsx")
# invoice = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/upload_3way/Invoice data_Updated.xlsx")
# resultDF, reslutSumm=threewaymatch(contract=contractDummy,po=po,invoice=invoice)
# print("result df :--", resultDF)
# print("result df :--", reslutSumm)
