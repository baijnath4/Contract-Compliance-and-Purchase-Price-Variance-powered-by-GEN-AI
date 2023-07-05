def contractandpo(contract,po):
    final_po = pd.merge(contract,po,how='inner',on=['Contract_ID','Line Item Description'])
    final_po = final_po[['POID','Line Item Description','SUPPLIER','PAYMENTTERMS_PO','POLINENUMBER','POQUANTITY','UNITOFMEASURE','UNITPRICEINORIGINALCURRENCY','POSPENDUSD','Contract_ID','Contracted Payterms','Contracted unit price']]
    final_po['Contracted Payterms'] = final_po['Contracted Payterms'].astype(int)
    final_po['Contracted unit price'] = final_po['Contracted unit price'].astype(int)
    final_po['PAYMENTTERMS_PO'] = final_po['PAYMENTTERMS_PO'].astype(int)
    final_po['UNITPRICEINORIGINALCURRENCY'] = final_po['UNITPRICEINORIGINALCURRENCY'].astype(int)
    final_po['Purchase Price variance(PO vs Contract)'] = ((final_po['UNITPRICEINORIGINALCURRENCY'] - final_po['Contracted unit price'])/final_po['Contracted unit price'])*100
    final_po['Purchase Price variance(PO vs Contract)'] = final_po['Purchase Price variance(PO vs Contract)'].astype(int)
    final_po['Payterm Difference (PO vs Contract)'] = (final_po['Contracted Payterms'] - final_po['PAYMENTTERMS_PO'])
    openai.api_key = ""
    prompt_s = ['provide the summary of the below data:']
    summary = ''
    summary+= (questions(final_po,prompt_s))    
    return final_po,summary