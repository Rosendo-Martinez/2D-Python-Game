import csv

class LeaderBoard:

    def __init__(self, filename):
        self._filename = filename
        self.index_of_last_replaced_row = None
    def get_rows(self):
        rows = None
        with open(self._filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            rows = []
            for row in csvreader:
                rows.append(row)
        return rows

    def save(self,round_number, game_time, kill_count):
        rows = []
        row_index_to_replace = None
        with open(self._filename,'r') as csvfile:
            csvreader = csv.reader(csvfile)
            rows.append(next(csvreader))
            i = 1
            for row in csvreader:
                rows.append(row)
                if row_index_to_replace == None:
                    if (int(row[0]) < round_number):
                        row_index_to_replace = i
                    elif (int(row[0]) == round_number):
                        if (int(row[2]) < kill_count):
                            row_index_to_replace = i
                i += 1

        self.index_of_last_replaced_row = row_index_to_replace
        with open(self._filename,'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            current_row_index = 0
            for row in rows:
                if row_index_to_replace == current_row_index:
                    csvwriter.writerow([round_number,game_time,kill_count])
                    current_row_index += 1
                if (current_row_index == 6):
                    break
                csvwriter.writerow(row)
                current_row_index += 1
