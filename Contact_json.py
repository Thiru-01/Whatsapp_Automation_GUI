import xlrd
import json

final_data = {}
valuesTodel = []
Location = "Your Contact Xcel file Path"

try:
    Workbook = xlrd.open_workbook(Location)
    Sheet = Workbook.sheet_by_index(0)

    for i in range(3, Sheet.nrows):
        data = Sheet.row_values(i, 1)
        for name in data[:1]:
            Num = []
            for num in Sheet.row_values(i, 2):
                if num == '':
                    pass
                else:
                    Num.append(num)
                final_data.update({name: Num})

    for i, j in final_data.items():
        if not j:
            valuesTodel.append(i)
    for v in valuesTodel:
        del final_data[v]

    json_object = json.dumps(final_data, indent=4)
    with open("Contact.json", "w") as outfile:
        outfile.write(json_object)
except Exception as e:
    print(e)
