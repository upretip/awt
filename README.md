# awt

This is an easy interface to provide the data from [Airport Wait Times](https://awt.cbp.gov) site in a pandas data frame. The AWT website can provide data for one year period max. ie. difference between `rptFrom` and `rptTo` can be up to 365 days, eg. from 3/1/2017 to 3/1/2018 is acceptable but 3/1/2019 - 3/1/2020 is not.

Usage
```
from awt import AWT

lax_awt = AWT(airport_id='LAX', date_from='03/01/2019', date_to='02/11/2020')
lax_scrape = lax_awt.get_data()
lax_df = lax_awt.clean_pandas(lax_scrape) # returns pandas dataframe

```
