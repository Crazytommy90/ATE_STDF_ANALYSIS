function InstallHDF5() {
    Write-Host "Installing HDF5..."
    Write-Host "ls C:/Program Files/7-zip"
    ls "C:/Program Files/7-zip"
    Start-Process "C:/Program Files/7-zip/7z.exe" -Wait -ArgumentList 'x ./hdf5-1.12.2-Std-win10_64-vs16.zip'
    ls
    cd hdf
    ls
    Write-Host "Installing HDF5-1.12.1..."
    Start-Process -FilePath msiexec.exe -ArgumentList "/quiet /qn /i HDF5-1.12.2-win64.msi" -Wait
    Write-Host "HDF5-1.12.1 installation complete"
}

function ModifyEnvironmentVariable() {
    $varName = "HDF5_DIR"
    $varValue = "C:\Program Files\HDF_Group\HDF5\1.12.1\cmake"
    #Write-Host "varName = $varName"
    #Write-Host "varValue = $varValue"
    ModifyMachineEnvironmentVariable $varName $varValue
}

function ModifyMachineEnvironmentVariable( $varName, $varValue ) {
    $target = "Machine"
    [Environment]::SetEnvironmentVariable($varName, $varValue, $target)
}

function main() {
    InstallHDF5
    ModifyEnvironmentVariable
}

main