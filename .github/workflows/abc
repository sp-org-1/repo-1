I am writing a workflow which has a step that runs a powershell script. In the script I generate the GitHub variable names dynamically whose value I want to fetch. But I am not able to refer to that dynamic variable name when fetching the value using `vars` context. 

```
foreach ($h in $uniqueValues.Keys) {
  Write-Output "*** $h";
  Write-Output "******** ${{ vars[format('{0}', '$h')] }}";
};
```

In the above code, I get list of three variables say SAAS_ART_EMAIL_MURTHY, SECRETKEY and ACCESSKEY. Out of these SAAS_ART_EMAIL_MURTHY is defined at the repo level. But when code is executed, I get empty value for both.

```
*** SAAS_ART_EMAIL_MURTHY
******** 
*** SECRETKEY
******** 
*** ACCESSKEY
******** 
```

I tried many different ways like "$h", "$$h", "\$h" but no luck. It either prints the empty string or gives syntax error.
Please help.
