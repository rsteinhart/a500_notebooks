# To get wget working with windows

1) Download from https://builtvisible.com/download-your-website-with-wget/

2) start powershell and make a bin directory to hold wget

`mkdir ~/bin`

3) copy wget into that folder as gget.exe

`cp ~/Downloads/wget.exe ~/bin/gget.exe`

4) edit your powershell profile in vscode:

`code $profile`

5) put ~/bin in your path by adding this to $profile:

`$Env:Path = "$HOME/bin;$Env:Path"`

6) close and restart powershell and download the zarr folder:

`gget -r https://clouds.eos.ubc.ca/~phil/docs/atsc500/data/bomex_timestep_53580.zarr`

# To get an informative prompt with powershell

1) open $profile with `code $profile`

2) add the function below so using a conda environment "work" in folder bin
will produce a prompt like 

`(work):Users/phil/bin`

```
function prompt 
{
    $l = Split-Path -leaf -path (Get-Location)
    $p = Split-Path -parent -path (Get-Location)
    $p = Split-path -leaf $p
    $e = Split-Path -leaf $env:conda_prefix
    write-host "($e):$p/$l"
    return "> "
}
```
