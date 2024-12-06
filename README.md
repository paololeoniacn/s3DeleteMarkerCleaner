# **S3 Delete Marker Manager**

### **Overview**
The **S3 Delete Marker Manager** is a Python-based application that provides an intuitive **Streamlit** interface for managing delete markers in Amazon S3 buckets. With this tool, you can list, select, and delete delete markers within a specific path of an S3 bucket, ensuring better control over your S3 storage.

This project is structured to streamline the setup and execution, requiring minimal configuration.

---

### **Project Structure**

```
s3-delete-marker-manager/
├── main.py                  # Main application logic with Streamlit
├── requirements.txt         # Python dependencies
├── run.ps1                  # PowerShell script to configure and launch the app
├── .env                     # Environment variables for AWS credentials (user-provided)
└── README.md                # Project documentation
```

---

### **Features**
- **Streamlit Web Interface**:
  - List delete markers in a specified bucket and path.
  - Interactive selection using checkboxes.
  - Delete selected markers with a single click.
- **Simple Setup**:
  - Automated virtual environment setup and dependency installation via `run.ps1`.
- **AWS Session Support**:
  - Works seamlessly with temporary AWS credentials (`AWS_SESSION_TOKEN`).

---

### **Setup Instructions**

#### **1. Prerequisites**
- **Python**: Version 3.8 or higher.
- **AWS Credentials**:
  - Ensure you have an `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` for authentication.
- **S3 Permissions**:
  - `s3:ListBucket`
  - `s3:GetObject`
  - `s3:DeleteObject`

#### **2. Clone the Repository**
```bash
git clone <repository_url>
cd s3-delete-marker-manager
```

#### **3. Create a `.env` File**
Add your AWS credentials to a `.env` file in the project root. The file should look like this:

```plaintext
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_SESSION_TOKEN=your_session_token
```

Ensure this file is added to `.gitignore` to prevent it from being tracked by version control.

#### **4. Run the Application**
Use the `run.ps1` PowerShell script to configure and launch the app:
```powershell
.\run.ps1
```

The script performs the following:
1. Removes any existing virtual environment.
2. Creates a new virtual environment.
3. Installs all required dependencies.
4. Launches the **Streamlit** application.

The application will start and be accessible in your browser at:
```
http://localhost:8501
```

---

### **Usage Instructions**

1. **Launch the App**:
   Run the `run.ps1` script as explained above.

2. **Configure the App**:
   - Enter the **S3 bucket name** and **path prefix** in the sidebar.
   - Click **"List Delete Markers"** to retrieve markers within the specified prefix.

3. **Select Markers**:
   - Use the checkboxes to select the delete markers you want to remove.

4. **Delete Selected Markers**:
   - Click **"Delete Selected Markers"** to remove them.

---

### **Dependencies**

The project relies on the following libraries:
- `boto3`: AWS SDK for Python.
- `python-dotenv`: For managing environment variables.
- `streamlit`: For the web interface.

Dependencies are automatically installed by `run.ps1`. Alternatively, you can manually install them using:
```bash
pip install -r requirements.txt
```

---

### **Security Best Practices**

1. **Environment Variables**:
   - Use the `.env` file to store sensitive AWS credentials.
   - Add `.env` to `.gitignore` to avoid exposing credentials in version control.

2. **Temporary Credentials**:
   - Use temporary AWS credentials (`AWS_SESSION_TOKEN`) whenever possible.

---

### **Known Limitations**
- **Large Buckets**:
  - Listing delete markers in large buckets with many versions may take time.
- **Pagination**:
  - Currently, the application does not support paginated results.

---

### **Potential Enhancements**
- **Pagination Support**:
  - Add pagination for buckets with a large number of delete markers.
- **Batch Processing**:
  - Enable faster operations by processing markers in bulk.

---

### **License**
This project is distributed under the MIT License. 

---

### **How the Code Handles Delete Markers**

The application focuses exclusively on delete markers in the bucket, thanks to the use of the `list_object_versions` method and the specific extraction of the `DeleteMarkers` field.

---

# **Focus**

Here's the critical part of the code where delete markers are handled:

```python
response = s3.list_object_versions(Bucket=bucket_name, Prefix=prefix)
return response.get("DeleteMarkers", [])
```

#### Key Points:

1. **`list_object_versions` Method**:
   - Lists all object versions and delete markers in the specified bucket.
   - The response includes fields such as:
     - `Versions`: Regular object versions.
     - `DeleteMarkers`: Only delete markers.
     - `CommonPrefixes`: Prefixes grouped if a delimiter is used.

2. **Extracting `DeleteMarkers`**:
   - By calling `response.get("DeleteMarkers", [])`, the code specifically retrieves only the delete markers, ignoring `Versions` and other fields.

3. **Prefix Filtering**:
   - The `Prefix=prefix` parameter narrows the results to the specified path.

---

### **Verification**

You can verify the response by logging the full result:

```python
response = s3.list_object_versions(Bucket=bucket_name, Prefix=prefix)

# Debugging output
st.write(response)  # Log to Streamlit UI
print(response)     # Log to console for CLI debugging

return response.get("DeleteMarkers", [])
```

#### Example Response
```json
{
  "DeleteMarkers": [
    {
      "Key": "example-file.txt",
      "VersionId": "11112222333344445555",
      "IsLatest": false,
      "LastModified": "2023-12-06T00:00:00.000Z",
      "Owner": {
        "ID": "owner-id"
      }
    }
  ],
  "Versions": [
    {
      "Key": "example-file.txt",
      "VersionId": "55554444333322221111",
      "IsLatest": true,
      "LastModified": "2023-12-01T00:00:00.000Z",
      "Size": 12345,
      "Owner": {
        "ID": "owner-id"
      }
    }
  ]
}
```

- **`DeleteMarkers`** contains only delete markers.
- **`Versions`** contains regular object versions.

---

### **Conclusion**

The code specifically accesses `response.get("DeleteMarkers", [])`, ensuring it focuses only on delete markers while ignoring other S3 object versions.