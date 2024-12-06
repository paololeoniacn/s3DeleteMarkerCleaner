import boto3
import os
from dotenv import load_dotenv
import streamlit as st


def list_delete_markers(bucket_name, prefix):
    """
    Lists all delete markers in a specific S3 bucket and path.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The specific path to filter objects.

    Returns:
        list: A list of delete markers with their key and version ID.
    """
    try:
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN")
        )
        s3 = session.client("s3")
        response = s3.list_object_versions(Bucket=bucket_name, Prefix=prefix)
        return response.get("DeleteMarkers", [])
    except Exception as e:
        st.error(f"Error while listing delete markers: {e}")
        return []


def delete_selected_markers(bucket_name, selected_markers):
    """
    Deletes selected delete markers from the specified S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        selected_markers (list): A list of dictionaries with 'Key' and 'VersionId'.
    """
    try:
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN")
        )
        s3 = session.client("s3")
        for marker in selected_markers:
            key = marker['Key']
            version_id = marker['VersionId']
            s3.delete_object(Bucket=bucket_name, Key=key, VersionId=version_id)
            st.success(f"Deleted marker for Key: {key}, Version ID: {version_id}")
    except Exception as e:
        st.error(f"Error while deleting markers: {e}")


def main():
    # Load environment variables from .env
    load_dotenv()

    # Validate AWS credentials
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY") or not os.getenv("AWS_SESSION_TOKEN"):
        st.error("AWS credentials (Access Key, Secret Key, and Session Token) are not set in the .env file.")
        return

    # Set page configuration
    st.set_page_config(
        page_title="S3 Delete Marker Manager",
        page_icon=":cloud:",
        layout="wide"
    )

    # Project title
    st.title("S3 Delete Marker Manager")
    st.markdown("### **Manage S3 delete markers effortlessly with precision and control.**")

    # Sidebar configuration
    st.sidebar.header("Configuration")

    # Input bucket name and prefix
    bucket_name = st.sidebar.text_input("S3 Bucket Name", "")
    prefix = st.sidebar.text_input("Path Prefix", "")

    # State management for delete markers
    if "delete_markers" not in st.session_state:
        st.session_state.delete_markers = []
    if "selected_markers" not in st.session_state:
        st.session_state.selected_markers = []

    # Button to list delete markers
    if st.sidebar.button("List Delete Markers"):
        if not bucket_name or not prefix:
            st.error("Bucket name and prefix are required.")
        else:
            st.info(f"Listing delete markers in bucket '{bucket_name}' with prefix '{prefix}'...")
            delete_markers = list_delete_markers(bucket_name, prefix)

            if not delete_markers:
                st.warning("No delete markers found.")
            else:
                st.session_state.delete_markers = delete_markers
                st.session_state.selected_markers = []
                st.success(f"Found {len(delete_markers)} delete markers.")

    # Display the list of delete markers
    if st.session_state.delete_markers:
        st.subheader("Delete Marker Management")

        # Display total and selected counters
        total_markers = len(st.session_state.delete_markers)
        selected_markers_count = len(st.session_state.selected_markers)
        st.info(f"Total Markers: {total_markers} | Selected: {selected_markers_count}")

        # Create 3 columns for the buttons
        col1, col2, col3 = st.columns(3)

        # Button to select all markers in the first column
        with col1:
            if st.button("Select All Markers"):
                st.session_state.selected_markers = st.session_state.delete_markers.copy()

        # Button to deselect all markers in the second column
        with col2:
            if st.button("Deselect All Markers"):
                st.session_state.selected_markers = []

        # Button to delete selected markers
        with col3:
            if st.button("Delete Selected Markers", type="primary"):
                if st.session_state.selected_markers:
                    st.info("Deleting selected delete markers...")
                    delete_selected_markers(bucket_name, st.session_state.selected_markers)
                    st.session_state.delete_markers = [m for m in st.session_state.delete_markers if m not in st.session_state.selected_markers]
                    st.session_state.selected_markers = []
                    st.success("Selected delete markers have been removed.")
                else:
                    st.warning("No markers selected for deletion.")
        
        # Individual checkboxes for each delete marker
        for marker in st.session_state.delete_markers:
            key = marker['Key']
            version_id = marker['VersionId']
            is_selected = marker in st.session_state.selected_markers

            if st.checkbox(f"{key} (Version ID: {version_id})", value=is_selected, key=f"{key}-{version_id}"):
                if marker not in st.session_state.selected_markers:
                    st.session_state.selected_markers.append(marker)
            else:
                if marker in st.session_state.selected_markers:
                    st.session_state.selected_markers.remove(marker)

        


if __name__ == "__main__":
    main()
