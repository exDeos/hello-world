def strip_excel_data(filepath):
    """Output a _tuple representing an Excel workbook's value contents.

Arguments:
filepath |  The path to the Excel workbook being captured.

_tuple structure is ((sheet_name, sheet_data), (...), ...)
sheet_name is the Worksheet.Name property of the COM interface.
sheet_data is the output of the COM UsedRange function for a Worksheet.
  This sheet_data is equivalent to a tuple (column) of tuples (rows)."""
    import win32com.client as pywincomclient
    xl = pywincomclient.DispatchEx("excel.application")
    xl.Visible = False
    wb = xl.Workbooks.Open(filepath, False, True)
    data = []
    for k in wb.Worksheets:
        data.append((k.Name, k.UsedRange()))
    wb.Close(False)
    return tuple(data)
