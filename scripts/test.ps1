param(
    # The access token to the GitHub Rest API 
    [Parameter(Mandatory=$true)]
    [string]
    $accessToken, 

    [Parameter(Mandatory=$true)]
    [string]
    $orgName,
    
    [Parameter(Mandatory=$true)]
    [string]
    $repoName
)

$authenticationToken = [System.Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$accessToken"))
$headers = @{
        "Authorization" = [String]::Format("token {0}", $authenticationToken)
        #"Authorization" = [String]::Format("Basic {0}", $accessToken)
        "Content-Type"  = "application/json"
}

$callUri = "https://api.github.com/orgs/$orgName/repos"
Write-Output $callUri

$repoVariables = Invoke-RestMethod -Method get -Uri $callUri -Headers $headers 
Write-Output $repoVariables

$callUri = "https://api.github.com/repos/$orgName/$repoName/actions/variables/APP_ID"
Write-Output $callUri

$repoVariables = Invoke-RestMethod -Method get -Uri $callUri -Headers $headers 
Write-Output $repoVariables

foreach ($variable in $repoVariables) {
    write-host  $variable.name
}

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
