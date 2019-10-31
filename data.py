import pandas as pd


df = pd.read_csv('Weerdata.txt', na_values=['     '], dtype={'STN':float,'YYYYMMDD': str,'DDVEC':float,'FHVEC':float,'FG':float,
    'FHX':float,'FHXH':float,'FHN':float,'FHNH':float,'FXX':float,'FXXH':float,'TG':float,'TN':float,'TNH':float,
    'TX':float,'TXH':float,'T10N':float,'T10NH':float,'SQ':float,'SP':float,'Q':float,'DR':float,'RH':float,'RHX':float,
    'RHXH':float,'PG':float,'PX':float,'PXH':float,'PN':float,'PNH':float,'VVN':float,'VVNH':float,'VVX':float,'VVXH':float,
    'NG':float,'UG':float,'UX':float,'UXH':float,'UN':float,'UNH':float,'EV24':float}, parse_dates=['YYYYMMDD'])

#df = pd.read_csv('Weerdata.txt', dtype={'STN':float,'YYYYMMDD': str}, parse_dates=['YYYYMMDD'])

#df.to_excel('file1.xlsx', )
#df.columns = ['STN, YYYYMMDD, HH, DD, FH, FF, FX, T, T10, TD, SQ, Q, DR,RH, P, VV, N, U, WW, IX, M, R, S, O, Y']
print(df.info())
#print(df)