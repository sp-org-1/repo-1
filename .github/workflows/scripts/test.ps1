$dlist = New-Object -TypeName 'System.Collections.ArrayList';
Select-String -Path "octopus.config" -Pattern '#{.*}' | ForEach-Object { 
    $value = $_.Matches.Value;
    $NewString = $value -replace "#{" -replace "}"
    #$uniqueValues[$NewString] = $true;
    if(! $dlist.Contains($NewString)) {
        $dlist.Add($NewString)
    }
}

Get-Content -Path octopus.config;
foreach($d in $dlist) {
    Write-Host "The current element is" $d
    (Get-Content octopus.config).Replace("#{$d}", 'MyValue') | Set-Content octopus.config;
}
Get-Content -Path octopus.config;
