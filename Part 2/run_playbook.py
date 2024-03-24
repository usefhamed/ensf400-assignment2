import ansible_runner
import requests


def run_playbook(playbook_name):
    project_dir = "/workspaces/ensf400-lab5-ansible"
    result = ansible_runner.run(private_data_dir=project_dir, playbook=playbook_name)

    if result:
        print(f"Playbook: {playbook_name} executed successfully.")
        print("Stats:", result.stats)
    else:
        print(f"ERROR! Could not run the playbook: {playbook_name}")


def verify_nodejs_responses():
    # Define the list of ports your NodeJS apps are running on
    nodejs_ports = [3000, 3001, 3002]

    for port in nodejs_ports:
        try:
            response = requests.get(f"http://localhost:{port}")
            if response.status_code == 200:
                print(f"Response from server on port {port}: {response.text.strip()}")
            else:
                print(
                    f"Server on port {port} did not return a 200 OK. Status Code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Request to server on port {port} failed with error: {e}")


def main():
    # Optionally run the hello.yml playbook
    run_playbook("hello.yml")

    # Verify the responses from the NodeJS servers
    verify_nodejs_responses()


if __name__ == "__main__":
    main()
