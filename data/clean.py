import pandas as pd
from datetime import datetime


class Dataset:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        data, date = [], None
        f = open("data/connections.csv", "r")
        for line in f:
            line = line.strip().split(",")
            if line[0].startswith("NYT Connections"):
                date = f"{line[1]}, {line[2]}"
            else:
                cat = line[0]
                w1, w2, w3, w4 = line[1], line[2], line[3], line[4]
                data.append([date, cat, w1, w2, w3, w4])
        f.close()
        df = pd.DataFrame(data, columns=["date", "category", "w1", "w2", "w3", "w4"])
        df["date"] = df["date"].apply(lambda x: self.convert_date(x))
        return df

    def convert_date(self, date_string) -> datetime:
        date, num, year = date_string.split(" ")

        num = (
            num.replace("st", "")
            .replace("nd", "")
            .replace("rd", "")
            .replace("th", "")
            .replace(",", "")
        )
        date_string = f"{date} {num}, {year}"
        return datetime.strptime(date_string, "%B %d, %Y")

    def write_clean_data(self) -> None:
        self.data.to_csv("data/connections_clean.csv", index=False)
