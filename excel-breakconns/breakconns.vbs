Dim cn As WorkbookConnection
Dim qr As WorkbookQuery
On Error Resume Next
For Each cn In ActiveWorkbook.Connections
cn.Delete
Next cn
For Each qr In ActiveWorkbook.Queries
qr.Delete
Next qr
