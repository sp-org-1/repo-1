$key = "1234567891234567" 
$textPassword = "securekey-textpassword"
$secureString = ConvertTo-SecureString -String $textPassword -AsPlainText -Force
$encryptedText = ConvertFrom-SecureString $secureString -Key (1..16)

$secureString = ConvertTo-SecureString $encryptedText -Key (1..16)
$plainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
)
Write-Output $plainText
Write-Host "textPassword: $textPassword"
Write-Host "encryptedText: $encryptedText"
Write-Host "plainText: $plainText"



#$b = (3,4,2,3,56,34,254,222,1,1,2,23,42,54,33,233,1,34,2,7,6,5,35,43)
#echo "======="
#echo $b
# Convert byte to string
#$str2 = [System.Text.Encoding]::UTF8.GetString($b)
#echo $str2
#$text = "Hello, this is a secret message"
#$secureString = ConvertTo-SecureString -String $text -AsPlainText -Force
#Write-Output $secureString
#$encryptedText = ConvertFrom-SecureString $secureString -Key $b
#Write-Output $encryptedText

#$secureString = ConvertTo-SecureString $encryptedText -Key $b
#$plainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
#    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
#)
#Write-Output $plainText