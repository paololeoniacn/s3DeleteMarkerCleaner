# Function to display colored messages
function Write-Color {
    param (
        [string]$Message,
        [ConsoleColor]$Color = "White"
    )
    $originalColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Message
    $Host.UI.RawUI.ForegroundColor = $originalColor
}

# Path to the virtual environment
$venvPath = ".\venv"

# if (Test-Path -Path $venvPath ) {
#     Write-Color "Removing existing {$venvPath}..." -Color Yellow
#     Remove-Item -Recurse -Force $venvPath 
# }

# Check if Python is installed
Write-Color "Checking if Python is installed..." -Color Yellow
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Color "Python is not installed or not in the PATH. Please install Python and try again." -Color Red
    exit 1
}

# Check if the virtual environment exists
if (!(Test-Path -Path $venvPath)) {
    Write-Color "Creating the virtual environment..." -Color Cyan
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Color "Failed to create the virtual environment. Check Python and try again." -Color Red
        exit 1
    }
}

# Activate the virtual environment
Write-Color "Activating the virtual environment..." -Color Green
& "$venvPath\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Color "Failed to activate the virtual environment. Check the path and try again." -Color Red
    exit 1
}

# Check for requirements.txt
$requirementsPath = ".\requirements.txt"
if (!(Test-Path -Path $requirementsPath)) {
    Write-Color "requirements.txt file not found. Please create one to specify dependencies." -Color Red
    deactivate
    exit 1
}

# Install dependencies from requirements.txt
Write-Color "Installing dependencies from requirements.txt..." -Color Yellow
pip install --upgrade pip
pip install -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    Write-Color "Failed to install dependencies. Check requirements.txt and try again." -Color Red
    deactivate
    exit 1
}

# Check if the Python script exists
$scriptPath = ".\main.py"
if (!(Test-Path -Path $scriptPath)) {
    Write-Color "main.py file not found. Ensure it is in the current directory." -Color Red
    deactivate
    exit 1
}

# Run Streamlit app
Write-Color "Starting Streamlit application..." -Color Cyan
streamlit run $scriptPath --server.headless true
if ($LASTEXITCODE -ne 0) {
    Write-Color "Failed to start the Streamlit application. Check for errors in the script." -Color Red
    deactivate
    exit 1
}

# Deactivate the virtual environment after exiting Streamlit
Write-Color "Deactivating the virtual environment..." -Color Green
deactivate

Write-Color "Streamlit application terminated successfully!" -Color Green
