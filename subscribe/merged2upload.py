import requests
import base64
import os

def fetch_and_decode_base64(url):
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        decoded_content = base64.b64decode(response.text)
        return decoded_content.decode('utf-8')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def upload_to_gist(content, gist_id, github_token):
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        "files": {
            "configsub.yaml": {
                "content": content
            }
        }
    }
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully updated Gist: {gist_id}")
    except requests.RequestException as e:
        print(f"Error updating Gist: {e}")

def main():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, 'data', 'subscribes.txt')
    
    with open(file_path, 'r') as file:
        urls = file.read().strip().split('\n')

    all_decoded_texts = []

    for url in urls:
        decoded_content = fetch_and_decode_base64(url)
        if decoded_content:
            all_decoded_texts.append(decoded_content)

    merged_content = "\n".join(all_decoded_texts)
    encoded_merged_content = base64.b64encode(merged_content.encode('utf-8')).decode('utf-8')

    merged_file_path = os.path.join(parent_dir, 'data', 'merged.txt')
    with open(merged_file_path, 'w') as file:
        file.write(encoded_merged_content)
        print(f"Encoded merged content written to {merged_file_path}")

    # Upload the merged content to the Gist 
    github_token = 'your github_token'
    gist_id = 'your gist_id'
    upload_to_gist(encoded_merged_content, gist_id, github_token)

if __name__ == "__main__":
    main()