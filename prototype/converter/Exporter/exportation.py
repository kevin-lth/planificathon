from openpyxl import Workbook
from openpyxl.utils.cell import range_boundaries
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json


filename = "super_planning.xlxs"

wk = Workbook()
sheet = wk.create_sheet(title='Feuil1')

sheet["B1"] = "hello"

wk.save(filename=filename)



