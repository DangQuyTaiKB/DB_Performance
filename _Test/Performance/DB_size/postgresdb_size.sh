# Set environment variables based on configuration (replace with actual values)
$frontend_url = "http://localhost:8000"
$gql_ug_url = "http://localhost:8000/gql"
$postgres_host = "postgres_gql"
$postgres_user = "postgres"
$postgres_password = "example"
$postgres_db = "data"

# Function to check database size (replace with your preferred method)
function Get-DatabaseSize {
  # Example using psql (assuming PostgreSQL and psql is installed)
  param (
    [string] $host,
    [int] $port,
    [string] $user,
    [string] $password,
    [string] $db
  )

  try {
    $process = Start-Process psql -ArgumentList "-h", $host, "-p", $port, "-U", $user, "-d", $db, "-c", "SELECT pg_database_size('$db');"
    $process.WaitForExit()
    $exitCode = $process.ExitCode
    if ($exitCode -eq 0) {
      $process.StandardOutput | ConvertTo-SingleLine
    } else {
      Write-Error "Error getting database size: Exit code $($exitCode)"
      return
    }
  } catch {
    Write-Error "Error getting database size: $_"
  }
}

# Get database size for the main database
$db_size = Get-DatabaseSize -host $postgres_host -port 5432 -user $postgres_user -password $postgres_password -db $postgres_db

# Write information to console
Write-Host "Frontend URL: $frontend_url"
Write-Host "GraphQL User Service URL: $gql_ug_url"
Write-Host "Database Size: $db_size bytes"

# Additional actions (can be added here based on your needs)

# Example: Send notification if database size exceeds a threshold
if ($db_size -gt 1073741824) { # 1 GB
  Write-Warning "Database size exceeds 1 GB!"
  # You can add logic to send notification here (e.g., email, logging)
}