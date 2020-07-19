import datetime as dt

import pandas as pd
import requests


class AWT:
    """Get airport wait time data from awt.cbp.gov website for the given time period.
    Maximum report range is one year"""

    URL = "https://awt.cbp.gov/"
    HEADERS = {
        "User-Agent": "AWT Robot git@github.com:upretip/awt",
        "DNT": "1",
        "Connection": "Keep-Alive",
    }

    payload = {
        "port": "A810",
        "rptFrom": "4/1/2020",
        "rptTo": "5/1/2020",
        "CreateReport": "Create+Report",
    }

    def __init__(self, airport_id: str, date_from: str, date_to: str):
        date_format = '%m/%d/%Y'
        date_from_converted = dt.datetime.strptime(date_from, date_format)
        date_to_converted = dt.datetime.strptime(date_to, date_format)
        date_diff = date_to_converted - date_from_converted
        assert date_diff.days < 366 and date_diff.days>0
        self.payload['port'] = airport_id
        self.payload['rptFrom'] = date_from
        self.payload['rptTo'] = date_to


    def get_data(self) -> str:
        r = requests.post(url=self.URL, headers=self.HEADERS, data=self.payload)
        try:
            if r.status_code == 200:
                return r.text
        except requests.RequestException as e:
            print(f"{e}")

    # def clean_bs4(self, html=self.get_data(payload)):
    #     """Use bs4 to clean the data into tables Not impletemnted"""
    #     pass

    def clean_pandas(self, html):
        """ Use pandas library to extrat the table on the given html page"""
        response_data = pd.read_html(html)[0]
        default_cols = [
            "airport",
            "terminal",
            "date",
            "hour",
            "citizen_avg_wait_time",
            "citizen_max_wait_time",
            "non_citizen_avg_wait_time",
            "non_citizen_max_wait_time",
            "all_avg_wait_time",
            "all_max_wait_time",
            "<15m",
            "15-30min",
            "30-45min",
            "45-60min",
            "60-90min",
            "90-120min",
            "120min<",
            "excluded",
            "total",
            "flights",
            "booths",
        ]
        response_data.columns = default_cols
        return response_data

    def sql_insert(self, conn, table):
        """write the data into a sql table given a connection"""
        pass


if __name__ == "__main__":
    from_date = '3/2/2019'
    to_date = '3/2/2020'
    awt = AWT(airport_id='LAX', date_from=from_date, date_to=to_date)
    scrape = awt.get_data()
    pd_df = awt.clean_pandas(scrape)
    print(pd_df.shape)
    print(pd_df.describe)
    print(pd_df.head(5))
