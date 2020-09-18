from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time
import csv
from csv import writer


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


class ARCTrack:
    def __init__(self):
        opts = Options()
        opts.set_headless()
        assert opts.headless  # Operating in headless mode'''
        self.browser = Chrome(options=opts)
    def start(self):
        import time
        url = 'https://apps2.campusrec.illinois.edu/checkins/live'
        self.browser.get(url)
        time.sleep(2)
        overallcapacity = self.browser.find_element_by_xpath('/html/body/div/div/div[1]/span[1]/span[1]').text.encode(
            "utf-8")
        datetimecollected = self.browser.find_element_by_xpath('/html/body/div/div/div[1]/span[2]/span').text.encode(
            "utf-8")
        opendataelems = self.browser.find_elements_by_xpath('/html/body/div/div/div[3]')
        closeddataelems = self.browser.find_elements_by_xpath('/html/body/div/div/div[5]')
        closetxtitems = [x.encode("utf-8") for x in closeddataelems[0].text.split("\n")]
        opentxtitems = [x.encode("utf-8") for x in opendataelems[0].text.split("\n")]
        datachunks = [opentxtitems[x:x + 5] for x in range(0, len(opentxtitems), 5)]
        closechunks = [closetxtitems[x:x + 3] for x in range(0, len(closetxtitems), 3)]
        for i in closechunks:
            i.insert(0, '0 %')
            i.insert(3, 'Last Count: 0')
            datachunks.append(i)
        filesize = os.path.getsize("./alldata.csv")
        if filesize == 0:
            cols = []
            cols.append("total_occupancy")
            cols.append("timestamp_collected")
            data = []
            data.append(overallcapacity)
            data.append(datetimecollected)
            for i in datachunks:
                cols.append(i[1].replace(" ", "_") + "_percentage_occupied")
                cols.append(i[1].replace(" ", "_") + "_open")
                cols.append(i[1].replace(" ", "_") + "_last_count")
                cols.append(i[1].replace(" ", "_") + "_timestamp")
                percentage = 0
                for z in i[0].split():
                    if z.isdigit():
                        percentage = float(z) / 100.00
                        break
                data.append(percentage)
                data.append(i[2])
                count = 0
                for z in i[3].split():
                    if z.isdigit():
                        count = int(z)
                        break
                data.append(count)
                data.append(i[4])
            data = [data]
            newtable = pd.DataFrame(data,columns=cols)
            newtable.to_csv('./alldata.csv',index=False)
        else:
            myrow = None
            with open('./alldata.csv') as f:
                reader = csv.reader(f)
                for row in reader:
                    # do something here with `row`
                    myrow = row
                    break
            print(myrow)
            data = []
            for i in datachunks:
                perce = myrow.index(i[1].replace(" ", "_") + "_percentage_occupied")
                opens = myrow.index(i[1].replace(" ", "_") + "_open")
                lastcount = myrow.index(i[1].replace(" ", "_") + "_last_count")
                time = myrow.index(i[1].replace(" ", "_") + "_timestamp")
                percentage = 0
                for z in i[0].split():
                    if z.isdigit():
                        percentage = float(z) / 100.00
                        break
                data.insert(perce,percentage)
                data.insert(opens,i[2])
                count = 0
                for z in i[3].split():
                    if z.isdigit():
                        count = int(z)
                        break
                data.insert(lastcount,count)
                data.insert(time,i[4])
            totals = myrow.index('total_occupancy')
            data.insert(totals,overallcapacity)
            times = myrow.index('timestamp_collected')
            data.insert(times,datetimecollected)
            append_list_as_row("./alldata.csv",data)
arcobj = ARCTrack()
arcobj.start()
