param (
    [string]$searchTerm
)

$query = "SELECT System.ItemName, System.ItemPathDisplay FROM SystemIndex WHERE System.ItemName LIKE '%$searchTerm%'"

$connection = New-Object -ComObject ADODB.Connection
$connection.Open("Provider=Search.CollatorDSO;Extended Properties='Application=Windows';")

$recordset = New-Object -ComObject ADODB.Recordset
$recordset.Open($query, $connection)

$results = @()
while (!$recordset.EOF) {
    $result = @{}
    foreach ($field in $recordset.Fields) {
        $result[$field.Name] = $field.Value
    }
    $results += $result
    $recordset.MoveNext()
}

$recordset.Close()
$connection.Close()

# Output JSON encoded in UTF-8
$results | ConvertTo-Json | Out-File -FilePath "output.json" -Encoding utf8
